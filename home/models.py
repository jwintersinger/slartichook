import os

class Work:
  @staticmethod
  def projects():
    filename = os.path.join(os.path.dirname(__file__), 'projects.txt').replace('\\', '/')
    return ProjectListParser(filename).parse()


class ProjectListParser:
  def __init__(self, filename):
    self._filename = filename
    self._read_raw_projects()

  def _read_raw_projects(self):
    src = open(self._filename)
    self._raw_projects = []
    for line in src:
      if not (line.startswith(' ') or line.startswith('\t') or line.strip() == ''):
        self._raw_projects.append('')
      self._raw_projects[-1] += line
    src.close()

  def parse(self):
    return [ProjectParser(project).parse() for project in self._raw_projects]


class ProjectParser:
  def __init__(self, raw_project):
    self._lines = [line.strip() for line in raw_project.strip().split('\n')]

  def parse(self):
    joiner = lambda lines: '\n'.join(lines)

    project = {
      'name':       self._lines.pop(0),
      'short_desc': joiner(self._read_until_blank()),
      'tidbits':    self._parse_tidbits(self._read_until_blank()),
      'long_desc':  joiner(self._lines),
    }
    project['id'] = self._format_id(project['name'])
    return project

  def _read_until_blank(self):
    idx = self._lines.index('')
    block = self._lines[:idx]
    self._lines = self._lines[idx:]

    # Remove any blank lines following the one we found.
    while self._lines[0] == '':
      self._lines.pop(0)

    return block

  def _parse_tidbits(self, raw_tidbits):
    tidbits = {}
    for line in raw_tidbits:
      name, values = line.split(':', 1)
      name = self._format_id(name)
      tidbits[name] = [value.strip() for value in values.split(',')]
    return tidbits

  def _format_id(self, label):
    return label.lower().replace(' ', '_').strip()
