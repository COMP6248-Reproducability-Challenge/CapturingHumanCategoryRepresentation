import os

# import http.server
# import socketserver
from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
# from flask.ext.jsonpify import jsonify
from joblib import dump, load

from chain import Chain
import markov

app = Flask(__name__)
api = Api(app)

n_chains = 4
chain_types = ['Man', 'Woman', 'Happy', 'Sad']

chains = {}


def generate_proposal(chain):
    # chain_key = '{}/{}'.format(chain_type, chain_id)
    # chain = chains[chain_key]
    print('z shape', chain.get_z().shape)
    new_z = markov.mutate(chain.get_z())
    # print(new_z)

    new_image = markov.generate(new_z)
    print(new_image.shape)
    index = len(chain)

    proposal_name = '{}/chain_{}/{}.jpg'.format(chain.type, chain.id, index)
    markov.save_image(new_image, 'static/images/' + proposal_name)
    chain.add_proposal(new_z, proposal_name)

    if index % 100 == 0:
        dump(chain, 'chain_data/{}/chain_{}/{}'.format(chain.type, chain.id, index))

    return proposal_name


def load_chain (type, id):
    loaded = True
    ch = None
    ind = 1
    while loaded:
        try:
            ch = load('chain_data/{}/chain_{}/{}'.format(type, id, ind * 100))
            print('Loaded chain:', '{}/chain_{}/{}'.format(type, id, ind * 100))
            ind += 1
        except FileNotFoundError:
            loaded = False

    return ch


def create_chain (type, id):
    chain = Chain(c, type)
    if not os.path.exists('static/images/{}/chain_{}'.format(type, id)):
        os.makedirs('static/images/{}/chain_{}'.format(type, id))

    if not os.path.exists('chain_data/{}/chain_{}'.format(type, id)):
        os.makedirs('chain_data/{}/chain_{}'.format(type, id))

    z = markov.noise()
    img = markov.generate(z)
    img_name = '{}/chain_{}/0.jpg'.format(type, id)
    markov.save_image(img, 'static/images/' + img_name)
    z = z.detach().numpy()
    chain.add_link(z, img_name)
    print(chain.type, chain.id)
    generate_proposal(chain)
    print('Created chain:', '{}/chain_{}'.format(type, id))
    return chain


for type in chain_types:
    for c in range(n_chains):
        chain = load_chain(type, c)
        if chain is None:
            chain = create_chain(type, c)

        chain_key = '{}/{}'.format(type, c)
        chains[chain_key] = chain

class Chain(Resource):
    def get(self):
        return {'chains': list(chains.keys())}


class ChainID(Resource):
    def get(self, chain_type, chain_id):
        # chain_type = request.args.get('type')
        chain_key = '{}/{}'.format(chain_type, chain_id)
        chain = chains[chain_key]
        chain_head = chain.get_image()
        if chain.proposal_image is None:
            proposal_name = generate_proposal(chain)
        else:
            proposal_name = chain.get_proposal()

        return { 'current': chain_head, 'proposal': proposal_name, 'steps': len(chain) - 1 }


class ChainAccept(Resource):
    def get(self, chain_type, chain_id):
        # chain_type = request.args.get('type')
        chain_key = '{}/{}'.format(chain_type, chain_id)
        chain = chains[chain_key]
        chain.accept_proposal()
        generate_proposal(chain)
        return { 'message': 'Proposal Accepted' }


class ChainReject(Resource):
    def get(self, chain_type, chain_id):
        # chain_type = request.args.get('type')
        chain_key = '{}/{}'.format(chain_type, chain_id)
        chain = chains[chain_key]
        chain.reject_proposal()
        generate_proposal(chain)
        return { 'message': 'Proposal Rejected' }


api.add_resource(Chain, '/chains')
api.add_resource(ChainID, '/types/<chain_type>/chains/<chain_id>')
api.add_resource(ChainAccept, '/types/<chain_type>/chains/<chain_id>/accept')
api.add_resource(ChainReject, '/types/<chain_type>/chains/<chain_id>/reject')


if __name__ == '__main__':
    host = '0.0.0.0' if os.environ.get('PYTHON_ENV') == 'PRODUCTION' else '127.0.0.1'
    print('env:', os.environ.get('PYTHON_ENV'))
    app.run(host=host, port='3000')
