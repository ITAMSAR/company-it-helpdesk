from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from apps.atk.models import (
    ATKDivisionStock,
    ATKItem,
    ATKRequest,
    get_stock_pool_division,
)


class Command(BaseCommand):
    help = 'Apply approved ATK requests into requester division stock when not applied yet.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--requester',
            help='Only sync approved requests for this username.',
        )

    def handle(self, *args, **options):
        source_division = get_stock_pool_division()
        if not source_division:
            self.stderr.write(self.style.ERROR('Divisi Administrator tidak ditemukan.'))
            return

        requests = (
            ATKRequest.objects
            .filter(status='approved', stock_applied_at__isnull=True)
            .select_related('requester__profile__division')
            .prefetch_related('lines__item')
            .order_by('created_at')
        )
        if options.get('requester'):
            requests = requests.filter(requester__username=options['requester'])

        applied = 0
        skipped = 0

        for atk_request in requests:
            target_division = getattr(getattr(atk_request.requester, 'profile', None), 'division', None)
            if not target_division:
                skipped += 1
                self.stderr.write(f'Skip request #{atk_request.pk}: requester belum punya divisi.')
                continue

            lines = [line for line in atk_request.lines.all() if line.item_id]
            if not lines and atk_request.item_id:
                lines = [atk_request]
            if not lines:
                skipped += 1
                self.stderr.write(f'Skip request #{atk_request.pk}: tidak ada item stok.')
                continue

            with transaction.atomic():
                can_apply = True
                for line in lines:
                    item = ATKItem.objects.select_for_update().get(pk=line.item_id)
                    if source_division != target_division:
                        source_stock, _ = ATKDivisionStock.objects.select_for_update().get_or_create(
                            item=item,
                            division=source_division,
                            defaults={'current_stock': 0, 'minimum_stock': 0}
                        )
                        if source_stock.current_stock < line.quantity:
                            can_apply = False
                            self.stderr.write(
                                f'Skip request #{atk_request.pk}: stok Admin {item.name} '
                                f'kurang ({source_stock.current_stock} < {line.quantity}).'
                            )
                            break

                if not can_apply:
                    skipped += 1
                    continue

                for line in lines:
                    item = ATKItem.objects.select_for_update().get(pk=line.item_id)
                    target_stock, _ = ATKDivisionStock.objects.select_for_update().get_or_create(
                        item=item,
                        division=target_division,
                        defaults={'current_stock': 0, 'minimum_stock': 0}
                    )
                    if source_division != target_division:
                        source_stock = ATKDivisionStock.objects.select_for_update().get(
                            item=item,
                            division=source_division,
                        )
                        source_stock.current_stock -= line.quantity
                        source_stock.save(update_fields=['current_stock', 'updated_at'])

                    target_stock.current_stock += line.quantity
                    target_stock.save(update_fields=['current_stock', 'updated_at'])
                    item.sync_global_stock_from_divisions()

                atk_request.stock_applied_at = timezone.now()
                atk_request.stock_applied_division = target_division
                atk_request.save(update_fields=['stock_applied_at', 'stock_applied_division', 'updated_at'])
                applied += 1

        self.stdout.write(self.style.SUCCESS(f'Applied: {applied}, skipped: {skipped}'))
