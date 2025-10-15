from agent_framework import Executor, WorkflowContext, handler, executor

class UpperCase(Executor):
    @handler
    async def to_upper_case(self, text: str, ctx: WorkflowContext[str]) -> None:
        """Convert the input to uppercase and forward it to the next node.

        Note: The WorkflowContext is parameterized with the type this handler will
        emit. Here WorkflowContext[str] means downstream nodes should expect str.
        """
        await ctx.send_message(text.upper())


# possible to create an executor from a function by using the @executor decorator:
@executor(id="upper_case_executor")
async def upper_case(text: str, ctx: WorkflowContext[str]) -> None:
    """Convert the input to uppercase and forward it to the next node.

    Note: The WorkflowContext is parameterized with the type this handler will
    emit. Here WorkflowContext[str] means downstream nodes should expect str.
    """
    await ctx.send_message(text.upper())


# possible to handle multiple input types by defining multiple handlers:
class SampleExecutor(Executor):
    @handler
    async def to_upper_case(self, text: str, ctx: WorkflowContext[str]) -> None:
        """Convert the input to uppercase and forward it to the next node.

        Note: The WorkflowContext is parameterized with the type this handler will
        emit. Here WorkflowContext[str] means downstream nodes should expect str.
        """
        await ctx.send_message(text.upper())

    @handler
    async def double_integer(self, number: int, ctx: WorkflowContext[int]) -> None:
        """Double the input integer and forward it to the next node.

        Note: The WorkflowContext is parameterized with the type this handler will
        emit. Here WorkflowContext[int] means downstream nodes should expect int.
        """
        await ctx.send_message(number * 2)

#  handler can use yield_output to produce outputs that will be considered 
#  as workflow outputs and be returned/streamed to the caller as an output event:
class SomeHandler1(Executor):
    @handler
    async def some_handler(message: str, ctx: WorkflowContext[Never, str]) -> None:
        await ctx.yield_output("Hello, World!")

class SomeHandler2(Executor):
    @handler
    async def some_handler(message: str, ctx: WorkflowContext) -> None:
        print("Doing some work...")

#  handler can use ctx.yield_error to yield an error that will be considered
#  as a workflow error and be returned/streamed to the caller as an error event:
class SomeHandler3(Executor):
    @handler
    async def some_handler(message: str, ctx: WorkflowContext) -> None:
        await ctx.yield_error("Something went wrong")       

#  handler can use ctx.send_message to send intermediate messages to downstream nodes:
class SomeHandler4(Executor):
    @handler
    async def some_handler(message: str, ctx: WorkflowContext[str]) -> None:
        await ctx.send_message("Intermediate message")
        await ctx.send_message("Final message")
        await ctx.yield_output("Done")

#  handler can use ctx.get_messages to receive messages from upstream nodes:
class SomeHandler5(Executor):
    @handler
    async def some_handler(ctx: WorkflowContext[str]) -> None:
        async for message in ctx.get_messages():
            print(f"Received message: {message}")   
        await ctx.yield_output("All messages processed")

#  handler can use ctx.get_all_messages to receive all messages from upstream nodes:
class SomeHandler6(Executor):
    @handler
    async def some_handler(ctx: WorkflowContext[str]) -> None:
        messages = await ctx.get_all_messages()
        for message in messages:
            print(f"Received message: {message}")   
        await ctx.yield_output("All messages processed")

#  handler can use ctx.get_last_message to receive the last message from upstream nodes:
class SomeHandler7(Executor):
    @handler
    async def some_handler(ctx: WorkflowContext[str]) -> None:
        message = await ctx.get_last_message()
        print(f"Received last message: {message}")   
        await ctx.yield_output("Last message processed")

#  handler can use ctx.close to close the context and stop receiving messages:
class SomeHandler8(Executor):
    @handler
    async def some_handler(ctx: WorkflowContext[str]) -> None:
        await ctx.close()
        await ctx.yield_output("Context closed")
        print("Context closed")
        # No more messages will be received after this point
        async for message in ctx.get_messages():
            print(f"Received message: {message}")
        print("This will never be printed")
        await ctx.yield_output("All messages processed")

#  handler can use ctx.is_closed to check if the context is closed:
class SomeHandler9(Executor):   
    @handler
    async def some_handler(ctx: WorkflowContext[str]) -> None:
        if ctx.is_closed():
            print("Context is closed")
            await ctx.yield_output("Context was already closed")
            return
        print("Context is open")
        await ctx.yield_output("Context is open")
        # Continue processing messages
        async for message in ctx.get_messages():
            print(f"Received message: {message}")
        await ctx.yield_output("All messages processed")
        print("All messages processed")
        # Close the context
        await ctx.close()
        print("Context closed")
        await ctx.yield_output("Context closed")
        # Check if the context is closed
        if ctx.is_closed():
            print("Context is now closed")
            await ctx.yield_output("Context is now closed")
        else:
            print("Context is still open")
            await ctx.yield_output("Context is still open") 
        # Attempt to receive more messages (will not receive any)
        async for message in ctx.get_messages():
            print(f"Received message: {message}")
        print("This will never be printed")
        await ctx.yield_output("No more messages will be received")
        await ctx.yield_output("All messages processed")
        print("All messages processed")
        await ctx.close()
        print("Context closed again")
        # No more messages will be received after this point
        async for message in ctx.get_messages():
            print(f"Received message: {message}")
        print("This will never be printed")
        await ctx.yield_output("All messages processed again")
        


