# Standard Library
import logging

# Third Party
import feedparser
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from dateutil import parser

# Django
from django.conf import settings
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

# Models
from podcasts.models import Episode

logger = logging.getLogger(__name__)

def save_new_episodes(feed, podcast_name):
    """Saves new episodes to the database.

    Checks the episode GUID against the episodes currently stored in the
    database. If not found, then a new `Episode` is added to the database.

    Args:
        feed: requires a feedparser object
        podcast_name: the name of the podcast
    """
    podcast_image = feed.channel.image["href"]

    for item in feed.entries:
        logger.info(f"Processing episode: {item.title} from {podcast_name}")
        if not Episode.objects.filter(guid=item.guid).exists():
            episode = Episode(
                title=item.title,
                description=item.description,
                pub_date=parser.parse(item.published),
                link=item.link,
                image=podcast_image,
                podcast_name=podcast_name,
                guid=item.guid,
            )
            episode.save()
            logger.info(f"Saved new episode: {episode.title} from {podcast_name}")
        else:
            logger.info(f"Episode already exists: {item.title} from {podcast_name}")

def fetch_and_save_episodes():
    """Fetches and saves new episodes from RSS for specified podcasts."""
    # Add new podcasts
    podcasts = [
        ("The Daily", "https://feeds.simplecast.com/54nAGcIl"),
        ("The Tim Ferriss Show", "https://tim.blog/feed/"),
        ("The Joe Rogan Experience", "https://joeroganexp.joerogan.libsynpro.com/rss"),
        ("Serial", "https://feeds.serialpodcast.org/serial"),
        ("This American Life", "https://feeds.thisamericanlife.org/thisamericanlife"),
        ("Planet Money", "https://www.npr.org/rss/podcast.php?id=510289"),
        ("My Dad Wrote a Porno", "https://feeds.acast.com/public/shows/mydadwroteaporno"),
    ]

    for podcast_name, feed_url in podcasts:
        logger.info(f"Fetching episodes for {podcast_name} from {feed_url}")
        _feed = feedparser.parse(feed_url)
        if _feed.bozo:
            logger.error(f"Failed to parse feed for {podcast_name}: {_feed.bozo_exception}")
        else:
            save_new_episodes(_feed, podcast_name)

def delete_old_job_executions(max_age=604_800):
    """Deletes all apscheduler job execution logs older than `max_age`."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)

class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            fetch_and_save_episodes,
            trigger="interval",
            minutes=2,
            id="Fetch and Save Episodes",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job: Fetch and Save Episodes.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="Delete Old Job Executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: Delete Old Job Executions.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
