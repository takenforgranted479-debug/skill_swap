from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from .models import SkillSwapRequest, SessionReview
from accounts.models import Notification

@receiver(post_save, sender=SkillSwapRequest)
def create_request_notification(sender, instance, created, **kwargs):
    """Create notification when a new skill swap request is created"""
    if created:
        # Create notification for the recipient
        Notification.objects.create(
            recipient=instance.recipient,
            notification_type='skill_request',
            title='New Skill Swap Request',
            message=f'{instance.requester.get_full_name() or instance.requester.username} wants to learn {instance.offered_skill.skill.name} from you.',
            related_user=instance.requester,
            related_object_id=instance.id
        )


@receiver(post_save, sender=SessionReview)
@receiver(post_delete, sender=SessionReview)
def update_ratings(sender, instance, **kwargs):
    """Update ratings when a review is saved or deleted"""
    from skills.models import OfferedSkill
    from accounts.models import UserProfile
    
    reviewee = instance.reviewee
    
    # Update the OfferedSkill ratings for the specific skill taught
    try:
        offered_skill = OfferedSkill.objects.get(
            user=reviewee, 
            skill=instance.session.skill,
            is_active=True
        )
        
        # Calculate average rating for this specific skill
        skill_reviews = SessionReview.objects.filter(
            reviewee=reviewee,
            session__skill=instance.session.skill,
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
        
    except OfferedSkill.DoesNotExist:
        pass
    
    # Update UserProfile overall ratings
    try:
        profile = UserProfile.objects.get(user=reviewee)
        
        # Calculate average rating as teacher (all skills)
        teacher_reviews = SessionReview.objects.filter(
            reviewee=reviewee,
            is_public=True
        )
        
        if teacher_reviews.exists():
            avg_teacher_rating = teacher_reviews.aggregate(avg=Avg('overall_rating'))['avg']
            profile.average_rating_as_teacher = avg_teacher_rating or 0
            profile.total_sessions_taught = teacher_reviews.count()
        else:
            profile.average_rating_as_teacher = 0
            profile.total_sessions_taught = 0
        
        # Calculate average rating as learner (reviews given to the user when they were learning)
        learner_reviews = SessionReview.objects.filter(
            reviewer=reviewee,
            is_public=True
        )
        
        if learner_reviews.exists():
            profile.total_sessions_learned = learner_reviews.count()
        else:
            profile.total_sessions_learned = 0
            
        profile.save()
        
    except UserProfile.DoesNotExist:
        pass