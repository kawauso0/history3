from text_processing import summarize_and_extract_prompts
from video_creator import create_video_from_images, generate_image_with_retry
from voicevox.speech_synthesis import create_sound_files_srt_files, concat_everything
from voicevox.voice import pyopenjtalk_synthesize

def main(input_text, detail_level, language, accuracy, painting_model, paint_style, openai_api_key):
    print(input_text)
    search_result = "検索結果：" + input_text
    prompts = []
    section_lists = []
    titles = []

    section_lists, prompts, titles = summarize_and_extract_prompts(input_text, detail_level, language, accuracy, paint_style, openai_api_key)

    print(section_lists)
    print(prompts)
    print(titles)

    durations = []
    durations = create_sound_files_srt_files(section_lists, titles)

    # 1次元配列に変換
    flattened_durations = [item for sublist in durations for item in sublist]
        
    image_urls_with_durations = [(generate_image_with_retry(prompt, painting_model), duration) for prompt, duration in zip(prompts, flattened_durations)]

    create_video_from_images(image_urls_with_durations, "output.mp4")

    concat_everything(section_lists)

    return search_result, section_lists, prompts, titles
