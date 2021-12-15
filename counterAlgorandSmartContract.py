from pyteal import *

'''
https://developer.algorand.org/docs/get-details/dapps/pyteal/
'''

def approval_program():

    handle_creation = Seq([
        App.globalPut(Bytes("Count"), Int(0)),
        Return(Int(1))
    ])

    scratch_count = ScratchVar(TealType.uint64)

    handle_opt_in = Return(Int(0))
    handle_close_out = Return(Int(0))
    handle_update = Return(Int(0))
    handle_delete = Return(Int(0))

    add = Seq([
        scratch_count.store(App.globalGet(Bytes("Count"))),
        App.globalPut(Bytes("Count"), scratch_count.load() + Int(1)),
        Return(Int(1))
    ])

    subtract = Seq([
        scratch_count.store(App.globalGet(Bytes("Count"))),
        If(scratch_count.load() > Int(0),
            App.globalPut(Bytes("Count"), scratch_count.load() - Int(1))
        ),
        Return(Int(1))
    ])

    handle_noop = Cond(
        [And(
            Global.group_size() == Int(1),
            Txn.application_args[0] == Bytes("Add")
        ), add],
        [And(
            Global.group_size() == Int(1),
            Txn.application_args[0] == Bytes("Subtract")
        ), subtract]
    )

    program = Cond(
        [Txn.application_id() == Int(0), handle_creation],
        [Txn.on_completion() == OnComplete.OptIn, handle_opt_in],
        [Txn.on_completion() == OnComplete.CloseOut, handle_close_out],
        [Txn.on_completion() == OnComplete.UpdateApplication, handle_update],
        [Txn.on_completion() == OnComplete.DeleteApplication, handle_delete],
        [Txn.on_completion() == OnComplete.NoOp, handle_noop]
    )
    return compileTeal(program, Mode.Application, version=5)

def clear_state_program():
    program = Return(Int(1))
    return compileTeal(program, Mode.Application, version=5)

print(approval_program())
print(clear_state_program())

