import azure.durable_functions as df

def orchestrator_function(context: df.DurableOrchestrationContext):
    input_data = context.get_input()

    blob_url = yield context.call_activity("fetch_data", input_data)
    chunk_urls = yield context.call_activity("split_data", blob_url)

    results = yield context.task_all([
        context.call_activity("process_data", url) for url in chunk_urls
    ])

    yield context.call_activity("save_results", results)
    return "Completed"

main = df.Orchestrator.create(orchestrator_function)
