import dagger
from dagger import function, object_type, DefaultPath, dag
import asyncio
from typing import Annotated

@object_type
class DaggerTest:
    @function
    async def build_and_run(self, source: Annotated[dagger.Directory, DefaultPath("/")]) -> dagger.Container:  # ✅ Must take 'self' as an argument
        # async with dagger.Connection() as client:
        #     src = client.directory() 
            # src = client.directory(".", include=["requirements.txt", "*.py"]) # ✅ Copy the entire project

            # Define the container
            container = (
                dag.container()
                .from_("python:3.10-slim")  # ✅ Use a slim Python image
                .with_workdir("/app")  # ✅ Set working directory
                .with_directory("/app", source)  # ✅ Copy all project files
                .with_exec(["ls", "-al", "/app"])
                .with_exec(["pip", "install", "--no-cache-dir", "-r", "requirements.txt"])  # ✅ Install dependencies
                .with_exposed_port(80)  # ✅ Expose port
                .with_exec(["python", "-m", "flask", "--app", "app.py", "run", "--host=0.0.0.0", "--port=80"])  # ✅ Start Flask
            )

            # ✅ Run the container
            result = await container.stdout()
            print(result)  # Print output

# ✅ Run the function
async def main():
    test = DaggerTest()
    await test.build_and_run()

if __name__ == "__main__":
    asyncio.run(main())
