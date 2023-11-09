#!/dev/null

from pprint import pprint

breakpoint()

code.interact(local=locals())

print("client_address .", self.client_address)
print("command        .", self.command)
print("path           .", self.path)
print("rfile          .", self.rfile)
print("wfile          .", self.wfile)
print("headers        ...")
print(self.headers)
print("...")
print()

print("address_string   .", self.address_string())
print("date_time_string .", self.date_time_string())
print("version_string   .", self.version_string())
print()

# send response without stderr log
self.send_response_only(404, "err0")

ruamel.yaml.YAML().dump(...)

# DEBUG_JSON = """{
#     "active": -1,
#     "nodes": [
#         [0, -1, "\\ud83c\\uddf7\\ud83c\\uddfa \\u4fc4\\u7f57\\u65af Edge", ""],
#         [1, -1, "\\ud83c\\uddf7\\ud83c\\uddfa \\u4fc4\\u7f57\\u65af IEPL [01] [Air]", ""],
#         [2, -1, "\\ud83c\\uddf7\\ud83c\\uddfa \\u4fc4\\u7f57\\u65af IEPL [02] [Air]", ""]
#     ]
# }"""

# DEBUG_JSON = """{
#     "active": -1,
#     "nodes": [
#         [0, -1, "\\ud83c", ""]
#     ]
# }"""

# self.wfile.write(DEBUG_JSON.encode())

