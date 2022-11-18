import ipfsapi
# Connect to local node


def uploadFile(filename):
    toReturn = ""
    try:
        api = ipfsapi.connect('127.0.0.1', 5001)
        print(api)
        new_file = api.add('./uploads/'+filename)
        print(new_file)
        toReturn = new_file['Hash']

    except ipfsapi.exceptions.ConnectionError as ce:
            print(str(ce))
            toReturn = "IPFS server not connected"
    return toReturn


if __name__ == '__main__':
    uploadFile("")