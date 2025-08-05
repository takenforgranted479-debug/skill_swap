from django.core.management.base import BaseCommand
from django.db.models import Avg
from skill_sessions.models import SessionReview
from skills.models import OfferedSkill
from accounts.models import UserProfile
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Update all rating calculations for existing data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting rating updates...'))
        
        # Update OfferedSkill ratings
        self.stdout.write('Updating OfferedSkill ratings...')
        updated_skills = 0
        
        for offered_skill in OfferedSkill.objects.filter(is_active=True):
            # Get reviews for this specific skill
            skill_reviews = SessionReview.objects.filter(
                reviewee=offered_skill.user,
                session__skill=offered_skill.skill,
                is_public=True
            )
            
            if skill_reviews.exists():
                avg_rating = skill_reviews.aggregate(avg=Avg('overall_rating'))['avg']
                offered_skill.average_rating = avg_rating or 0
                offered_skill.total_sessions = skill_reviews.count()
            else:
                offered_skill.average_rating = 0
                offered_skill.total_sessions = 0
            
            offered_skill.save()
            updated_skills += 1
        
        self.stdout.write(f'Updated {updated_skills} offered skills')
        
        # Update UserProfile ratings
        self.stdout.write('Updating UserProfile ratings...')
        updated_profiles = 0
        
        for user in User.objects.all():
            try:
                profile = user.profile
            except UserProfile.DoesNotExist:
                continue
            
            # Calculate average rating as teacher (all skills)
            teacher_reviews = SessionReview.objects.filter(
                reviewee=user,
                is_public=True
            )
            
            if teacher_reviews.exists():
                avg_teacher_rating = teacher_reviews.aggregate(avg=Avg('overall_rating'))['avg']
                profile.average_rating_as_teacher = avg_teacher_rating or 0
                profile.total_sessions_taught = teacher_reviews.count()
            else:
                profile.average_rating_as_teacher = 0
                profile.total_sessions_taught = 0
            
            # Calculate sessions learned (reviews given by the user)
            learner_reviews = SessionReview.objects.filter(
                reviewer=user,
                is_public=True
            )
            
            profile.total_sessions_learned = learner_reviews.count()
            
            profile.save()
            updated_profiles += 1
        
        self.stdout.write(f'Updated {updated_profiles} user profiles')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully updated all ratings!')
        )