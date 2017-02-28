import base64
from email import message_from_file
from io import StringIO

str = "TUlNRS1WZXJzaW9uOiAxLjANClJlY2VpdmVkOiBieSAxMC4xMi4xNzEuOTIgd2l0aCBIVFRQOyBXZWQsIDE2IE5vdiAyMDE2IDA2OjM4OjQxIC0wODAwIChQU1QpDQpEYXRlOiBXZWQsIDE2IE5vdiAyMDE2IDIwOjA4OjQxICswNTMwDQpEZWxpdmVyZWQtVG86IGdvd3RoYW1hbmQ3QGdtYWlsLmNvbQ0KTWVzc2FnZS1JRDogPENBSz1wZmpkN2tMTVM0aTJvcmhyOVF0ZG96VUZPMGY1c0otRnU2Nytob0NheHg0NHdQUUBtYWlsLmdtYWlsLmNvbT4NClN1YmplY3Q6IEtpbmQgYXR0ZW50aW9uIHRvIE1hbmFnaW5nIGRpcmVjdG9yDQpGcm9tOiBHb3d0aGFtYW4gVGhhbmdhdmVsIDxnb3d0aGFtYW5kN0BnbWFpbC5jb20-DQpUbzogc2FsZXNAYmhhcmF0LW1vdG9ycy5jb20NCkNvbnRlbnQtVHlwZTogbXVsdGlwYXJ0L2FsdGVybmF0aXZlOyBib3VuZGFyeT05NGViMmMwZTY0Njg3ZjE4NDMwNTQxNmMwN2QzDQoNCi0tOTRlYjJjMGU2NDY4N2YxODQzMDU0MTZjMDdkMw0KQ29udGVudC1UeXBlOiB0ZXh0L3BsYWluOyBjaGFyc2V0PVVURi04DQpDb250ZW50LVRyYW5zZmVyLUVuY29kaW5nOiBxdW90ZWQtcHJpbnRhYmxlDQoNCj1FMj04MD04Qj1FMj04MD04Qg0KSGkgU2lyLA0KDQpNeXNlbGYgR293dGhhbWFuIGZyb20gUG9sbGFjaGksIEkgaGF2ZSBib29rZWQgcm95YWwgZW5maWxlZCBjbGFzc2ljIDM1MA0Kc2lsdmVyIG9uIE5vdiAybmQsIDIwMTYsIEFuZCBteSBib29raW5nIGlkIGlzIEJLTkc2MTc5MTYxNzAwNzE5Lg0KDQpJIG1hZGUgYm9va2luZyBhdCBCSEFSQVQgTU9UT1JTIFBvbGxhY2hpLA0KDQpUb2RheSBJIHJlY2VpdmVkIGEgY2FsbCBmcm9tIHRoZSBzaG93cm9vbSBmb3IgdGhlIGF2YWlsYWJpbGl0eSBvZiBteSBiaWtlLg0KU28gd2UgYXJyYW5nZWQgdGhlIG1vbmV5IGFzIGhhcmQgY2FzaCAoZnVsbCBhbW91bnQpIGFuZCB3ZW50IHRvIHRoZQ0Kc2hvd3Jvb20gd2l0aCBhIG1lY2hhbmljIChmcmllbmQgZm9yIG1lKSB0byBpbnNwZWN0IHRoZSBiaWtlLiBCdXQgYmVmb3JlDQpzaG93IHRoZSBiaWtlLCB0aGUgc2hvd3Jvb20gbWFuYWdlciBhc2sgdXMgdG8gcGF5IHRoZSBhbW91bnQsIGhlIHNhaWQsIGhlDQp3aWxsIHNob3cgdGhlIGJpa2UgYWZ0ZXIgdGhlIHBheW1lbnQuIFRoZXkgZGlkIHNvbWUgcGFwZXJ3b3JrIGFmdGVyIHdlIHBhaWQNCjEsNDMsMDAwIGFzIGNhc2guDQoNCldlIGZvdW5kIHRoZSBiaWtlIGFsbG9jYXRlZCBmb3IgbWUgaGFzIGlzc3VlcyBbc291bmQgb2YgdGhlIGJpa2UgbG9va3MNCmRpZmZlcmVudCAodG9vIG5vaXN5IGFuZCBpdCdzIG5vdCBvcmRpbmFyeSBSRSBzb3VuZCldIGZvdW5kIGJ5IGJvdGggb3VyDQptZWNoYW5pYyBhbmQgdGhlIG1lY2hhbmljIGluIHRoZSBzaG93cm9vbS4gU28gd2UgYXNrZWQgdGhlIG1hbmFnZXIgdG8gKnByb3Y9DQppZGUNCmFueSBvdGhlciBiaWtlKiB3aGljaCBhcmUgc3RhbmRpbmcgb3V0IHRoZXJlLCAqaWYgbm90Kiogd2UgYXJlIHJlYWR5IHRvDQp3YWl0IGFub3RoZXIgb25lIG1vbnRoKi4NCg0KUGxlYXNlIHJlZnVuZCB0aGUgY2FzaCBhbW91bnQgd2UgcGFpZC4gV2Ugd2lsbCBwYXkgaXQgd2hlbiB3ZSByZWNlaXZlIHRoZQ0KbmV3IGJpa2UuDQoNCklmIGl0IGlzIG5vdCByZXNvbHZlZCB3aXRoaW4gMyBkYXlzLCB3ZSBkb24ndCBoYXZlIGFueSBvcHRpb24gb3RoZXIgdGhhbg0KZXNjYWxhdGluZyB0aGlzIHRvIFJveWFsIEVuZmllbGQgTWFuYWdlbWVudC4NCg0KDQotLQ0KVGhhbmtzICYgUmVnYXJkcywNCkdvd3RoYW1hbiBUaGFuZ2F2ZWwNCg0KLS05NGViMmMwZTY0Njg3ZjE4NDMwNTQxNmMwN2QzDQpDb250ZW50LVR5cGU6IHRleHQvaHRtbDsgY2hhcnNldD1VVEYtOA0KQ29udGVudC1UcmFuc2Zlci1FbmNvZGluZzogcXVvdGVkLXByaW50YWJsZQ0KDQo8ZGl2IGRpcj0zRCJsdHIiPjxkaXYgY2xhc3M9M0QiZ21haWxfZGVmYXVsdCIgc3R5bGU9M0QiZm9udC1mYW1pbHk6dmVyZGFuYSw9DQpzYW5zLXNlcmlmO2ZvbnQtc2l6ZTpzbWFsbCI-PUUyPTgwPThCPUUyPTgwPThCPC9kaXY-PGRpdiBjbGFzcz0zRCJnbWFpbF9kZWY9DQphdWx0IiBzdHlsZT0zRCJmb250LWZhbWlseTp2ZXJkYW5hLHNhbnMtc2VyaWY7Zm9udC1zaXplOnNtYWxsIj5IaSBTaXIsPC9kaXY9DQo-PGRpdiBjbGFzcz0zRCJnbWFpbF9kZWZhdWx0IiBzdHlsZT0zRCJmb250LWZhbWlseTp2ZXJkYW5hLHNhbnMtc2VyaWY7Zm9udC09DQpzaXplOnNtYWxsIj48YnI-PC9kaXY-PGRpdiBjbGFzcz0zRCJnbWFpbF9kZWZhdWx0IiBzdHlsZT0zRCJmb250LXNpemU6c21hbGw9DQoiPjxkaXYgY2xhc3M9M0QiZ21haWxfZGVmYXVsdCIgc3R5bGU9M0QiZm9udC1mYW1pbHk6YXJpYWwsc2Fucy1zZXJpZiI-PGZvbnQ9DQogZmFjZT0zRCJ2ZXJkYW5hLCBzYW5zLXNlcmlmIiBjb2xvcj0zRCIjMDAwMDAwIj5NeXNlbGYgR293dGhhbWFuIGZyb20gUG9sbGE9DQpjaGksPUMyPUEwSSBoYXZlIGJvb2tlZCByb3lhbCBlbmZpbGVkIGNsYXNzaWMgMzUwIHNpbHZlciBvbiBOb3YgMm5kLCAyMDE2LCA9DQpBbmQgbXkgYm9va2luZyBpZCBpcz1DMj1BMEJLTkc2MTc5MTYxNzAwNzE5Lj1DMj1BMDwvZm9udD48L2Rpdj48ZGl2IGNsYXNzPQ0KPTNEImdtYWlsX2RlZmF1bHQiIHN0eWxlPTNEImZvbnQtZmFtaWx5OmFyaWFsLHNhbnMtc2VyaWYiPjxmb250IGZhY2U9M0QidmVyPQ0KZGFuYSwgc2Fucy1zZXJpZiIgY29sb3I9M0QiIzAwMDAwMCI-PGJyPjwvZm9udD48L2Rpdj48ZGl2IGNsYXNzPTNEImdtYWlsX2RlPQ0KZmF1bHQiIHN0eWxlPTNEImZvbnQtZmFtaWx5OmFyaWFsLHNhbnMtc2VyaWYiPjxmb250IGZhY2U9M0QidmVyZGFuYSwgc2Fucy1zPQ0KZXJpZiIgY29sb3I9M0QiIzAwMDAwMCI-SSBtYWRlIGJvb2tpbmcgYXQ9QzI9QTBCSEFSQVQgTU9UT1JTIFBvbGxhY2hpLD1DMj0NCj1BMDwvZm9udD48L2Rpdj48ZGl2IGNsYXNzPTNEImdtYWlsX2RlZmF1bHQiIHN0eWxlPTNEImZvbnQtZmFtaWx5OmFyaWFsLHNhbj0NCnMtc2VyaWYiPjxmb250IGZhY2U9M0QidmVyZGFuYSwgc2Fucy1zZXJpZiIgY29sb3I9M0QiIzAwMDAwMCI-PGJyPjwvZm9udD48Lz0NCmRpdj48ZGl2IGNsYXNzPTNEImdtYWlsX2RlZmF1bHQiIHN0eWxlPTNEImZvbnQtZmFtaWx5OmFyaWFsLHNhbnMtc2VyaWYiPjxmbz0NCm50IGZhY2U9M0QidmVyZGFuYSwgc2Fucy1zZXJpZiIgY29sb3I9M0QiIzAwMDAwMCI-VG9kYXkgSSByZWNlaXZlZCBhIGNhbGwgZj0NCnJvbSB0aGUgc2hvd3Jvb20gZm9yIHRoZSBhdmFpbGFiaWxpdHkgb2YgbXkgYmlrZS4gU28gd2UgYXJyYW5nZWQgdGhlIG1vbmV5ID0NCmFzIGhhcmQgY2FzaCAoZnVsbCBhbW91bnQpIGFuZCB3ZW50IHRvIHRoZSBzaG93cm9vbSB3aXRoIGEgbWVjaGFuaWMgKGZyaWVuZD0NCiBmb3IgbWUpIHRvIGluc3BlY3QgdGhlIGJpa2UuIEJ1dCBiZWZvcmUgc2hvdyB0aGUgYmlrZSwgdGhlIHNob3dyb29tIG1hbmFnZT0NCnIgYXNrIHVzIHRvIHBheSB0aGUgYW1vdW50LCBoZSBzYWlkLCBoZSB3aWxsIHNob3cgdGhlIGJpa2U9QzI9QTA8L2ZvbnQ-PHNwYT0NCm4gc3R5bGU9M0QiY29sb3I6cmdiKDAsMCwwKTtmb250LWZhbWlseTp2ZXJkYW5hLHNhbnMtc2VyaWYiPmFmdGVyIHRoZSBwYXltZT0NCm50PC9zcGFuPjxzcGFuIHN0eWxlPTNEImNvbG9yOnJnYigwLDAsMCk7Zm9udC1mYW1pbHk6dmVyZGFuYSxzYW5zLXNlcmlmIj4uID0NClRoZXkgZGlkIHNvbWUgcGFwZXJ3b3JrIGFmdGVyIHdlIHBhaWQgMSw0MywwMDAgYXMgY2FzaC48L3NwYW4-PC9kaXY-PGRpdiBjbD0NCmFzcz0zRCJnbWFpbF9kZWZhdWx0IiBzdHlsZT0zRCJmb250LWZhbWlseTphcmlhbCxzYW5zLXNlcmlmIj48Zm9udCBmYWNlPTNEIj0NCnZlcmRhbmEsIHNhbnMtc2VyaWYiIGNvbG9yPTNEIiMwMDAwMDAiPjxicj48L2ZvbnQ-PC9kaXY-PGRpdiBjbGFzcz0zRCJnbWFpbD0NCl9kZWZhdWx0Ij48Zm9udCBjb2xvcj0zRCIjMDAwMDAwIiBmYWNlPTNEInZlcmRhbmEsIHNhbnMtc2VyaWYiPldlIGZvdW5kIHRoZT0NCiBiaWtlIGFsbG9jYXRlZCBmb3IgbWUgaGFzIGlzc3VlcyBbPC9mb250PjxzcGFuIHN0eWxlPTNEImNvbG9yOnJnYigwLDAsMCk7Zj0NCm9udC1mYW1pbHk6dmVyZGFuYSxzYW5zLXNlcmlmIj48c3BhbiBzdHlsZT0zRCJmb250LXN0eWxlOml0YWxpYyI-c291bmQgb2YgdD0NCmhlIGJpa2UgbG9va3MgZGlmZmVyZW50ICh0b28gbm9pc3kgYW5kIGl0JiMzOTtzIG5vdCBvcmRpbmFyeT1DMj1BMFJFIHNvdW5kKT0NCjwvc3Bhbj5dPC9zcGFuPjxzcGFuIHN0eWxlPTNEImNvbG9yOnJnYigwLDAsMCk7Zm9udC1mYW1pbHk6dmVyZGFuYSxzYW5zLXNlcj0NCmlmIj49QzI9QTBmb3VuZCBieSBib3RoIG91ciBtZWNoYW5pYyBhbmQgdGhlIG1lY2hhbmljIGluIHRoZSBzaG93cm9vbS49QzI9DQo9QTA8L3NwYW4-PHNwYW4gc3R5bGU9M0QiY29sb3I6cmdiKDAsMCwwKTtmb250LWZhbWlseTp2ZXJkYW5hLHNhbnMtc2VyaWYiPlM9DQpvIHdlIGFza2VkIHRoZSBtYW5hZ2VyIHRvPUMyPUEwPC9zcGFuPjxzcGFuIHN0eWxlPTNEImNvbG9yOnJnYigwLDAsMCk7Zm9udC09DQpmYW1pbHk6dmVyZGFuYSxzYW5zLXNlcmlmIj48aT5wcm92aWRlIGFueSBvdGhlciBiaWtlPC9pPjwvc3Bhbj48c3BhbiBzdHlsZT0NCj0zRCJjb2xvcjpyZ2IoMCwwLDApO2ZvbnQtZmFtaWx5OnZlcmRhbmEsc2Fucy1zZXJpZiI-PUMyPUEwd2hpY2ggYXJlIHN0YW5kaT0NCm5nIG91dCB0aGVyZSwgPGk-aWYgbm90PC9pPjwvc3Bhbj48c3BhbiBzdHlsZT0zRCJjb2xvcjpyZ2IoMCwwLDApO2ZvbnQtZmFtaT0NCmx5OnZlcmRhbmEsc2Fucy1zZXJpZiI-PGk-PUMyPUEwd2UgYXJlIHJlYWR5IHRvIHdhaXQgYW5vdGhlciBvbmUgbW9udGg8L2k-PD0NCi9zcGFuPjxzcGFuIHN0eWxlPTNEImNvbG9yOnJnYigwLDAsMCk7Zm9udC1mYW1pbHk6dmVyZGFuYSxzYW5zLXNlcmlmIj4uPC9zcD0NCmFuPjwvZGl2PjxkaXYgY2xhc3M9M0QiZ21haWxfZGVmYXVsdCI-PHNwYW4gc3R5bGU9M0QiY29sb3I6cmdiKDAsMCwwKTtmb250LT0NCmZhbWlseTp2ZXJkYW5hLHNhbnMtc2VyaWYiPjxicj48L3NwYW4-PC9kaXY-PGRpdiBjbGFzcz0zRCJnbWFpbF9kZWZhdWx0Ij48cz0NCnBhbiBzdHlsZT0zRCJjb2xvcjpyZ2IoMCwwLDApO2ZvbnQtZmFtaWx5OnZlcmRhbmEsc2Fucy1zZXJpZiI-UGxlYXNlIHJlZnVuZD0NCiB0aGUgY2FzaCBhbW91bnQgd2UgcGFpZC4gV2Ugd2lsbCBwYXkgaXQgd2hlbiB3ZSByZWNlaXZlIHRoZSBuZXcgYmlrZS48L3NwYT0NCm4-PC9kaXY-PGRpdiBjbGFzcz0zRCJnbWFpbF9kZWZhdWx0Ij48c3BhbiBzdHlsZT0zRCJjb2xvcjpyZ2IoMCwwLDApO2ZvbnQtZj0NCmFtaWx5OnZlcmRhbmEsc2Fucy1zZXJpZiI-PGJyPjwvc3Bhbj48L2Rpdj48ZGl2IGNsYXNzPTNEImdtYWlsX2RlZmF1bHQiPjxmbz0NCm50IGNvbG9yPTNEIiMwMDAwMDAiIGZhY2U9M0QidmVyZGFuYSwgc2Fucy1zZXJpZiI-SWYgaXQgaXMgbm90IHJlc29sdmVkIHdpdD0NCmhpbiAzIGRheXMsIHdlIGRvbiYjMzk7dCBoYXZlIGFueSBvcHRpb24gb3RoZXIgdGhhbiBlc2NhbGF0aW5nIHRoaXMgdG8gUm95YT0NCmwgRW5maWVsZCBNYW5hZ2VtZW50LjwvZm9udD48L2Rpdj48ZGl2IHN0eWxlPTNEImZvbnQtZmFtaWx5OnZlcmRhbmEsc2Fucy1zZT0NCnJpZiI-PGZvbnQgY29sb3I9M0QiIzAwMDAwMCIgZmFjZT0zRCJ2ZXJkYW5hLCBzYW5zLXNlcmlmIj48YnI-PC9mb250PjwvZGl2Pj0NCjwvZGl2Pj1DMj1BMDxicj48ZGl2IGNsYXNzPTNEImdtYWlsLW1fNTE0OTczMTE2OTM5OTExMzY2OGdtYWlsX3NpZ25hdHVyZSI-PD0NCmRpdiBkaXI9M0QibHRyIj48ZGl2PjxkaXYgZGlyPTNEImx0ciI-PGRpdj48ZGl2IGRpcj0zRCJsdHIiPjxkaXY-PGZvbnQgZmFjZT0NCj0zRCJ2ZXJkYW5hLCBzYW5zLXNlcmlmIiBzaXplPTNEIjIiPjxzcGFuIHN0eWxlPTNEImNvbG9yOnJnYigxMzYsMTM2LDEzNikiPj0NCi0tPC9zcGFuPjwvZm9udD48L2Rpdj48ZGl2Pjxmb250IGZhY2U9M0QidmVyZGFuYSwgc2Fucy1zZXJpZiIgc2l6ZT0zRCIyIj48cz0NCnBhbiBzdHlsZT0zRCJjb2xvcjpyZ2IoMTM2LDEzNiwxMzYpIj5UaGFua3MgJmFtcDsgUmVnYXJkcyw8L3NwYW4-PC9mb250PjwvZD0NCml2PjxkaXY-PGZvbnQgZmFjZT0zRCJ2ZXJkYW5hLCBzYW5zLXNlcmlmIiBzaXplPTNEIjIiPjxzcGFuIHN0eWxlPTNEImNvbG9yOj0NCnJnYigxMzYsMTM2LDEzNikiPkdvd3RoYW1hbiBUaGFuZ2F2ZWw8L3NwYW4-PC9mb250Pjxicj48L2Rpdj48L2Rpdj48L2Rpdj48Lz0NCmRpdj48L2Rpdj48L2Rpdj48L2Rpdj4NCjxicj48YnI-PGJyPjxpbWcgd2lkdGg9M0QiMCIgaGVpZ2h0PTNEIjAiIGNsYXNzPTNEIm1haWx0cmFjay1pbWciIHNyYz0zRCJodD0NCnRwczovL21haWx0cmFjay5pby90cmFjZS9tYWlsL2FiNDY1YmRmOTM1ZTMwNmY3YzNhZmY1M2Y0YmM1YTRiMzMyY2ZmODMucG5nPz0NCnU9M0Q4MDcxNTYiPjwvZGl2Pg0KDQotLTk0ZWIyYzBlNjQ2ODdmMTg0MzA1NDE2YzA3ZDMtLQ=="

orginal_response = base64.urlsafe_b64decode(str)
orginal_response = orginal_response.decode("utf-8")
b = message_from_file(StringIO(orginal_response))
mp = b.is_multipart()
if b.is_multipart():
    for payload in b.get_payload():
        # if payload.is_multipart(): ...
        print(payload.get_payload())
else:
    print(b.get_payload())
print(mp)