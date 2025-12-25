from analytics import Research, Analytics, setup_logging
import config
import logging
import sys

def format_forecast(predictions, numbers_dict):
    """Переделывает данные в человеко-читабельный формат"""
    logging.info("Formatting forecast for report")

    tails_count = sum(1 for p in predictions if p == [0, 1] or str(p) == "0, 1")
    heads_count = len(predictions) - tails_count

    tails_word = numbers_dict.get(tails_count, str(tails_count))
    heads_word = numbers_dict.get(heads_count, str(heads_count))

    tail_suffix = "" if tails_count == 1 else "s"
    head_suffix = "" if heads_count == 1 else "s"

    if tails_count == 0:
        forecast = f"{heads_word} head{tail_suffix}"
    elif heads_count == 0:
        forecast = f"{tails_word} tail{tail_suffix}"
    else:
        forecast = f"{tails_word} tail{tail_suffix} and {heads_word} head{head_suffix}"

    logging.debug(f"Formatted forecast: {forecast}")
    return forecast

def main():
    try:
        logging.info("Starting report generation...")

        # Инициализируется класс ресёрчера
        researcher = Research()
        logging.info(f"Research initialized with file: {researcher.path}")

        # Получаются данные из файла
        data = researcher.file_reader()
        logging.info(f"Successfully read {len(data)} lines from file")

        # Готовятся данные для обработки анализатором
        data_for_analysis = data[1:] if researcher.has_header else data
        logging.info(f"Analyzing {len(data_for_analysis)} data points")

        # Инициализируется анализатор
        analyzer = Analytics(data_for_analysis)
        logging.info("Analytics instance created")

        # Вычисляется статистика
        num_observations = len(data_for_analysis)
        heads, tails = analyzer.counts_arg
        head_frac, tail_frac = analyzer.fractions()

        logging.info(f"Statistics: observations={num_observations}, heads={heads}, tails={tails}")
        logging.info(f"Fractions: heads={head_frac:.4f}, tails={tail_frac:.4f}")

        # Генерируются предсказания
        predictions = analyzer.predict_random(config.num_of_steps)
        logging.info(f"Generated {len(predictions)} predictions")

        # Словарь для чисел
        numbers = {
            0: "zero", 1: "one", 2: "two", 3: "three", 4: "four",
            5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine",
            10: "ten", 11: "eleven", 12: "twelve"
        }

        forecast = format_forecast(predictions, numbers)

        report = config.report_template.format(
            num_observations=num_observations,
            num_heads=numbers.get(heads, str(heads)),
            num_tails=numbers.get(tails, str(tails)),
            head_prob=round(head_frac * 100, 2),
            tail_prob=round(tail_frac * 100, 2),
            num_steps=config.num_of_steps,
            forecast=forecast
        )

        logging.info("Report template populated")

        # Сохраняется доклад
        saved_file = analyzer.save_file(report, 'report', 'txt')
        logging.info(f"Report saved to {saved_file}")

        # Выводится доклад в консоль
        print(report)
        print()

        message = "The report has been successfully created"
        success = researcher.send_telegram_message(message, config)

        if success:
            logging.info("Success notification sent to Telegram")
        else:
            logging.warning("Failed to send success notification to Telegram")

        logging.info("Report generation completed SUCCESSFULLY!")

    except Exception as e:
        error_msg = f"The report hasn't been created due to an error: {str(e)}"
        logging.error(error_msg)

        try:
            researcher.send_telegram_message(error_msg, config)
        except:
            pass

        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()