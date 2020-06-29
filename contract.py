from solc import compile_standard

compiled_sol = compile_standard({
    'language': 'Solidity',
    'sources': {
        'HashStorage.sol': {
            'content': '''
                pragma solidity >=0.4.16 <0.7.0;

                contract HashStorage {
                    mapping(uint => address) registeredHashes;

                    function registerHash(uint hash) public returns (bool success) {
                        if (registeredHashes[hash] != address(0)) {
                          return false;
                        }
                        registeredHashes[hash] = msg.sender;
                    }

                    function getOwner(uint hash) public view returns (address) {
                        return registeredHashes[hash];
                    }
                }
            ''',
        }
    },
    'settings': {
        'outputSelection': {
            '*': {
                '*': [
                    "metadata", "evm.bytecode", "evm.bytecode.sourceMap"
                ]
            }
        }
    },
})
