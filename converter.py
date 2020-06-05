#!/usr/bin/env python3
#pylint: disable=anomalous-backslash-in-string
"""
Export Dayone JSON Files to html"
"""
import json
import sys
import base64
import re
import markdown

def get_base64_by_id(photos, identifier):
    """
    Return the Base64 of the photo
    """
    if identifier in photos:
        pdata = photos[identifier]
        image_path = './photos/{}.{}'.format(pdata['md5'], pdata['type'])
        with open(image_path, 'rb') as photo_raw:
            photo_base64 = base64.b64encode(photo_raw.read()).decode('ascii')
            return "data:image/{};base64,{}".format(pdata['type'], photo_base64)
    return ""

def main():
    """
    Parse Json
    """

    filename = sys.argv[1]
    out_foldername = "./out"

    template_start = "<html><meta charset='utf-8'><head></head><body>"
    template_end = "</body></html>"


    raw_data = json.loads(open(filename).read())
    for entry in raw_data['entries']:
        out_filename = "{}/{}.html".format(out_foldername, entry['creationDate'])
        photos = {}
        with open(out_filename, 'w+') as outfile:
            outfile.write(template_start)
            if 'photos' in entry:
                photos = {x['identifier']:x for x in entry['photos']}

            if 'text' in entry:
                text = markdown.markdown(entry['text'])
                for image_id in re.findall('\"dayone-moment:\/\/([A-Za-z0-9]+)', text):
                    text = text.replace('dayone-moment://'+image_id, get_base64_by_id(photos,
                                                                                      image_id))

                outfile.write(text)
            if 'location' in entry:
                outfile.write("<li><b>Location</b> {} </li>".format(entry['location']))
            outfile.write("</ul>")
            outfile.write(template_end)

if __name__ == "__main__":
    print("Start exporter...")
    main()
    print("...Done")
