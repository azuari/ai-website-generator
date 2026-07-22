from flask import Response
import io
import zipfile


def download_html(html_code):
    """
    Download generated website as HTML
    """

    return Response(
        html_code,
        mimetype="text/html",
        headers={
            "Content-Disposition":
            "attachment; filename=generated_website.html"
        }
    )


def download_zip(html_code):
    """
    Download generated website as ZIP
    """

    memory_file = io.BytesIO()

    with zipfile.ZipFile(
        memory_file,
        mode="w",
        compression=zipfile.ZIP_DEFLATED
    ) as zf:

        zf.writestr(
            "index.html",
            html_code
        )

    memory_file.seek(0)

    return Response(
        memory_file.read(),
        mimetype="application/zip",
        headers={
            "Content-Disposition":
            "attachment; filename=generated_website.zip"
        }
    )