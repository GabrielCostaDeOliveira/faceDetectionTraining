import os


def main():
    for t in ['train', 'val']:
        # Run this file inside src directory
        with open(f'../dataset/wider_face_split/wider_face_{t}_bbx_gt.txt', 'r') as f:
            fn = ''
            preds = []
            for row in f.readlines():
                row = row.strip()
                if row.endswith('.jpg'):
                    if fn:
                        fn, _ = fn.rsplit('.', 1)
                        os.makedirs(f'../dataset/WIDER_{t}/annotations/{fn.rsplit("/",1)[0]}', exist_ok=True)
                        with open(f'../dataset/WIDER_{t}/annotations/{fn}.txt', 'w') as w:
                            w.write('\n'.join(preds))
                        print(f'finished file {fn}')
                    fn = row
                    preds = []
                if len(row.split()) > 5:
                    preds.append(row)


if __name__ == '__main__':
    main()
