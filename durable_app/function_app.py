import azure.functions as func
import azure.durable_functions as df

async def main(req: func.HttpRequest, starter: str):
    client = df.DurableOrchestrationClient(starter)
    instance_id = await client.start_new("orchestrator", None, req.get_json())
    return client.create_check_status_response(req, instance_id)
