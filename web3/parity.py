from typing import (
    List,
    Optional,
    Union,
)

from eth_typing import (
    Address,
    ChecksumAddress,
    Hash32,
    HexStr,
)
from eth_utils import (
    is_checksum_address,
)
from eth_utils.toolz import (
    assoc,
)

from web3._utils.compat import (
    Literal,
)
from web3._utils.personal import (
    ec_recover,
    ecRecover,
    import_raw_key,
    importRawKey,
    list_accounts,
    listAccounts,
    new_account,
    newAccount,
    send_transaction,
    sendTransaction,
    sign,
    sign_typed_data,
    signTypedData,
    unlock_account,
    unlockAccount,
)
from web3._utils.rpc_abi import (
    RPC,
)
from web3.module import (
    Module,
    ModuleV2,
)
from web3.types import (
    ENS,
    BlockIdentifier,
    EnodeURI,
    ParityBlockTrace,
    ParityFilterParams,
    ParityFilterTrace,
    ParityMode,
    ParityNetPeers,
    ParityTraceMode,
    TxParams,
    _Hash32,
)


class ParityPersonal(ModuleV2):
    """
    https://wiki.parity.io/JSONRPC-personal-module
    """
    ec_recover = ec_recover
    import_raw_key = import_raw_key
    list_accounts = list_accounts
    new_account = new_account
    send_transaction = send_transaction
    sign = sign
    sign_typed_data = sign_typed_data
    unlock_account = unlock_account
    # deprecated
    ecRecover = ecRecover
    importRawKey = importRawKey
    listAccounts = listAccounts
    newAccount = newAccount
    sendTransaction = sendTransaction
    signTypedData = signTypedData
    unlockAccount = unlockAccount


class Parity(Module):
    """
    https://paritytech.github.io/wiki/JSONRPC-parity-module
    """
    _default_block: Literal["latest"] = "latest"  # noqa: E704
    personal: ParityPersonal

    @property
    def default_block(self) -> str:
        return self._default_block

    @property
    def defaultBlock(self) -> str:
        warnings.warn(
            'defaultBlock is deprecated in favor of default_block',
            category=DeprecationWarning,
        )
        return self._default_block

    def enode(self) -> EnodeURI:
        return self.web3.manager.request_blocking(
            RPC.parity_enode,
            [],
        )

    def list_storage_keys(
        self,
        address: Union[Address, ChecksumAddress, ENS],
        quantity: int,
        hash_: Hash32,
        block_identifier: Optional[BlockIdentifier] = None,
    ) -> List[Hash32]:
        if block_identifier is None:
            block_identifier = self.default_block
        return self.web3.manager.request_blocking(
            RPC.parity_listStorageKeys,
            [address, quantity, hash_, block_identifier],
        )

    def net_peers(self) -> ParityNetPeers:
        return self.web3.manager.request_blocking(
            RPC.parity_netPeers,
            [],
        )

    def add_reserved_peer(self, url: EnodeURI) -> bool:
        return self.web3.manager.request_blocking(
            RPC.parity_addReservedPeer,
            [url],
        )

    def trace_replay_transaction(
        self, transaction_hash: _Hash32, mode: ParityTraceMode = ['trace']
    ) -> ParityBlockTrace:
        return self.web3.manager.request_blocking(
            RPC.trace_replayTransaction,
            [transaction_hash, mode],
        )

    def trace_replay_block_transactions(
        self, block_identifier: BlockIdentifier, mode: ParityTraceMode = ['trace']
    ) -> List[ParityBlockTrace]:
        return self.web3.manager.request_blocking(
            RPC.trace_replayBlockTransactions,
            [block_identifier, mode]
        )

    def trace_block(self, block_identifier: BlockIdentifier) -> List[ParityBlockTrace]:
        return self.web3.manager.request_blocking(
            RPC.trace_block,
            [block_identifier]
        )

    def trace_filter(self, params: ParityFilterParams) -> List[ParityFilterTrace]:
        return self.web3.manager.request_blocking(
            RPC.trace_filter,
            [params]
        )

    def trace_transaction(self, transaction_hash: _Hash32) -> List[ParityFilterTrace]:
        return self.web3.manager.request_blocking(
            RPC.trace_transaction,
            [transaction_hash]
        )

    def trace_call(
        self,
        transaction: TxParams,
        mode: ParityTraceMode = ['trace'],
        block_identifier: Optional[BlockIdentifier] = None
    ) -> ParityBlockTrace:
        # TODO: move to middleware
        if 'from' not in transaction and is_checksum_address(self.web3.eth.defaultAccount):
            transaction = assoc(transaction, 'from', self.web3.eth.defaultAccount)

        # TODO: move to middleware
        if block_identifier is None:
            block_identifier = self.default_block
        return self.web3.manager.request_blocking(
            RPC.trace_call,
            [transaction, mode, block_identifier],
        )

    def trace_raw_transaction(
        self, raw_transaction: HexStr, mode: ParityTraceMode = ['trace']
    ) -> ParityBlockTrace:
        return self.web3.manager.request_blocking(
            RPC.trace_rawTransaction,
            [raw_transaction, mode],
        )

    def set_mode(self, mode: ParityMode) -> bool:
        return self.web3.manager.request_blocking(
            RPC.parity_setMode,
            [mode]
        )

    def mode(self) -> ParityMode:
        return self.web3.manager.request_blocking(
            RPC.parity_mode,
            []
        )
