import settings


def handle_uploader(self, folder, file_name, open_file, cnt_type):
    file = settings.PROJECT_DIR / folder / file_name
    if not file.exists():
        return self.handle_404()
    with file.open(open_file) as fp:
        fl = fp.read()

    self.respond(fl, content_type=cnt_type)