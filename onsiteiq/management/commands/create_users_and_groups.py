from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand

from authentication.models import User


class Command(BaseCommand):
    help = "Creates the users and groups"

    def handle(self, *args, **options):
        view_permission = Permission.objects.get(codename="can_view_applicant")
        create_permission = Permission.objects.get(codename="can_add_applicant")
        change_status_permission = Permission.objects.get(
            codename="can_change_applicant_status"
        )
        add_note_permission = Permission.objects.get(codename="can_add_applicant_note")

        admin_group = Group.objects.create(name="admins")
        admin_group.permissions.add(view_permission)
        admin_group.permissions.add(create_permission)
        admin_group.permissions.add(change_status_permission)
        admin_group.permissions.add(add_note_permission)
        admin_user = User.objects.create(username="admin", password="admin")
        admin_user.groups.add(admin_user)
        admin_user.save()

        adjudicator_group = Group.objects.create(name="adjudicators")
        adjudicator_group.permissions.add(view_permission)
        adjudicator_group.permissions.add(change_status_permission)
        adjudicator_group.permissions.add(add_note_permission)
        adjudicator_user = User.objects.create(
            username="adjudicator", password="adjudicator"
        )
        adjudicator_user.groups.add(adjudicator_group)
        adjudicator_user.save()

        contributor_group = Group.objects.create(name="contributors")
        contributor_group.permissions.add(view_permission)
        contributor_group.permissions.add(add_note_permission)
        contributor_user = User.objects.create(
            username="contributor", password="contributor"
        )
        contributor_user.groups.add(contributor_group)
        contributor_user.save()

        viewer_group = Group.objects.create(name="viewers")
        viewer_group.permissions.add(view_permission)
        viewer_user = User.objects.create(username="viewer", password="viewer")
        viewer_user.groups.add(viewer_group)
        viewer_user.save()
