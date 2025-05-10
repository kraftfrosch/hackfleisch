from dotenv import load_dotenv
import os
from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    openai,
    cartesia,
    deepgram,
    noise_cancellation,
    silero,
    bey
)
from livekit.plugins.turn_detector.multilingual import MultilingualModel
# from livekit.plugins.bey import start_bey_avatar_session
load_dotenv(override=True)
from datetime import datetime
import json
import argparse
SURVEY_PROMPT = ""
SURVEY_ID = ""
class ConversationBot(Agent):
    def __init__(self, system_prompt: str) -> None:
        super().__init__(instructions=system_prompt)
        self.conversation_history = []

        print(f"System prompt: {system_prompt}")
        
    async def on_connect(self, session: AgentSession):
        # Initialize conversation with system prompt
        self.conversation_history = [{"role": "system", "content": self.instructions}]
        await session.generate_reply(
            instructions="Tell the user about the survey and ask them to start the survey."
        )
    
    async def on_message(self, session: AgentSession, message: str):
        # Add user message to history
        self.conversation_history.append({"role": "user", "content": message})
        
        # Get response from OpenAI
        response = await openai.chat.completions.create(
            model="gpt-4o",
            messages=self.conversation_history
        )
        
        # Extract and send the response
        assistant_message = response.choices[0].message.content
        self.conversation_history.append({"role": "assistant", "content": assistant_message})
        await session.generate_reply(instructions=assistant_message)




def function_creator(SURVEY_PROMPT: str, SURVEY_ID: str):
    SURVEY_PROMPT = SURVEY_PROMPT
    SURVEY_ID = SURVEY_ID

    async def entrypoint(ctx: agents.JobContext):
        async def write_transcript():
            ## Check if a survey directory exists
            if not os.path.exists(f"Transcript/{SURVEY_ID}"):
                os.makedirs(f"Transcript/{SURVEY_ID}")

            current_date = datetime.now().strftime("%Y%m%d_%H%M%S")
            # This example writes to the temporary directory, but you can save to any location
            filename = f"Transcript/{SURVEY_ID}/transcript_{ctx.room.name}_{current_date}.json"
            
            with open(filename, 'w') as f:
                json.dump(local_agent_session.history.to_dict(), f, indent=2)
                
            print(f"Transcript for {ctx.room.name} saved to {filename}")

        ctx.add_shutdown_callback(write_transcript)
        await ctx.connect()

        ## Use a male voice
        local_agent_session  = AgentSession(
            stt=deepgram.STT(model="nova-3", language="multi"),
            llm=openai.LLM(model="gpt-4"),
            tts=cartesia.TTS(),
            vad=silero.VAD.load(),
            turn_detection=MultilingualModel(),
        )

        # Create conversation bot with custom system prompt
        bot = ConversationBot(
            system_prompt=f"""You are an assistant who is supposed to conduct the survey on the following: {SURVEY_PROMPT}"""
        )

        bey_avatar_session = bey.AvatarSession()

        await bey_avatar_session.start(local_agent_session, room=ctx.room)
        await local_agent_session.start(
            room=ctx.room,
            agent=bot,
            room_input_options=RoomInputOptions(
                noise_cancellation=noise_cancellation.BVC(),
            ),
        )

    return entrypoint


if __name__ == "__main__":

    ## Take cli arguments
    # parser = argparse.ArgumentParser(description='Run the video agent.')
    # parser.add_argument('--survey_prompt', type=str, required=True, help='The prompt for the survey')
    # parser.add_argument('--survey_id', type=str, required=True, help='The id for the survey')
    # args = parser.parse_args()

    # ## Set the survey prompt and id
    # SURVEY_PROMPT = args.survey_prompt
    # SURVEY_ID = args.survey_id

    SURVEY_PROMPT = "You are supposed to conduct a survey on CDTM."
    SURVEY_ID = "1"
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=function_creator(SURVEY_PROMPT, SURVEY_ID)))