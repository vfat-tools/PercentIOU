import json
import pytest


@pytest.fixture(autouse=True)
def isolation_setup(fn_isolation):
    # enable function isolation
    pass


@pytest.fixture(scope="module")
def deployer(accounts):
    return accounts[0]


@pytest.fixture(scope="module")
def percentIOU(PercentIOU, tree, deployer):
    return PercentIOU.deploy("PercentIOU", "PIOU", tree["tokenTotal"], {"from": deployer})


@pytest.fixture(scope="module")
def tree():
    with open("snapshot/02-merkle.json") as fp:
        claim_data = json.load(fp)
    for value in claim_data["claims"].values():
        value["amount"] = int(value["amount"], 16)

    return claim_data


@pytest.fixture(scope="module")
def distributor(MerkleDistributor, tree, percentIOU, deployer):
    contract = MerkleDistributor.deploy(
        percentIOU, tree["merkleRoot"], {"from": deployer}
    )
    percentIOU.transfer(contract, tree["tokenTotal"])

    return contract
