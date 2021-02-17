from bs4 import BeautifulSoup
import requests

def download_shapes(output_dir):
    for i in ['1'] + [chr(x) for x in range(ord('a'), ord('z'))]:
        soup = BeautifulSoup(requests.get("https://conwaylife.com/ref/lexicon/lex_%s.htm" % i).text, 'html.parser')
        sp = soup.find_all(['p', 'pre'])

        for ln in range(len(sp)):
            link = sp[ln]
            if link.name == "pre" and len(link.find_all('a')) == 0 and sp[ln-1].b:
                shape_name = sp[ln-1].b.text.replace("/", "_")
                shape_body = "\n".join([line.strip() for line in link.text.split()])
                with open("%s/%s" % (output_dir, shape_name), "w") as f:
                    f.write(shape_body)
            
if __name__ == "__main__":
    download_shapes("shapes")