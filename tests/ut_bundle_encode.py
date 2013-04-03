import repyhelper
repyhelper.translate_and_import('bundle.repy')

strings = [
  'hello world',
  'testing 1234567890 ~!@#$%^&*()_+',
  '\r\n\n\xff'
]

for string in strings:
  if _bundle_embed_decode(_bundle_embed_encode(string)) != string:
    print "Encoding/Decoding failed for string:", string
    print _bundle_embed_decode(_bundle_embed_encode(string))