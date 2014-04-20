from django.core import management
from django_cron import CronJobBase, Schedule

class ParseFeedsCronJob(CronJobBase):
	RUN_EVERY_MINS = 10
	ALLOW_PARALLEL_RUNS = False

	schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
	code = 'feeds.parse_feeds_cron_job'

	def do(self):
		print('Start ParseFeedsCronJob.')
		management.call_command('parsefeeds')