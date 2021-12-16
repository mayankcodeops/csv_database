form_html = """
<form action="/upload_csv" method="post" enctype="multipart/form-data">
  <input type="text" name="file-name" value="report">
  <input type="file" name="myFile">
  <button type="submit">Submit</button>
</form>
"""
