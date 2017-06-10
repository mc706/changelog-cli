from invoke import Collection

from tasks.test import test
from tasks.lint import lint
from tasks.release import release

ns = Collection()
ns.add_task(test)
ns.add_task(lint)
ns.add_task(release)
