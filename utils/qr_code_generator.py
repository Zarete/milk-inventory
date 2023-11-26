import argparse
import uuid

import qrcode

parser = argparse.ArgumentParser(
    prog='QR Code Generator',
    description='Generate QR codes with unique UUID (v4) identifier'
)

parser.add_argument('-c', help='Number of QR code to generate', dest='count', type=int)

args = parser.parse_args()


def generate_uuid4(count: int) -> list[str]:
    return [str(uuid.uuid4()) for _ in range(count)]


def generate_qrcodes(uuids: list[str]) -> None:
    for generated_uuid in uuids:
        qrcode.make(generated_uuid).save(f'{generated_uuid}.png')


def main():
    uuids = generate_uuid4(args.count)
    generate_qrcodes(uuids)


if __name__ == '__main__':
    main()
