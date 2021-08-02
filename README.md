# pygofile [![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fgautamajay52%2Fpygofile&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://github.com/gautamajay52/pygofile)

> Asynchronous Python Wrapper for the GoFile API (Unofficial).

### Installation :
```bash
pip3 install pygofile
```

### Usage :
```python
>> from pygofile import Gofile

>> gofile = Gofile(token='<YOUR_TOKEN>') # <YOUR_TOKEN> is your GoFile token

# or

>> gofile = Gofile() # as a guest

# to upload
>> data = await gofile.upload(file='/path/to/file.ext')

>> print(data)
{'downloadPage': 'https://gofile.io/d/OF8ctM', 'code': 'OF8ctM', 'parentFolder': '7a5cd11e-6fa34dda-44-bab5-c57d74d28d', 'fileId': 'e72b3dab-9190-48a0-9abe-89e45d1c0', 'fileName': 'file.ext', 'md5': '0aff68c0c302e07a52f4a1fbc5a687b', 'directLink': 'https://srv-store5.gofile.io/download/e72b3ab-9abe-8901c45d1c0/file.ext', 'info': 'Direct links only work if your account is a donor account. Standard accounts will have their links redirected to the download page.'}

>> download_url = data['downloadPage']

>> await gofile.delete_content(content_id='e72b3dab-9190-48a0-9abe-89e45d1c0')
```
### Credits: ⚡
* [GautamKumar(me)](https://github.com/gautamajay52) for [Nothing](https://github.com/gautamajay52/pygofile)