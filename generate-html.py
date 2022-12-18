
import os


prefix = '../model_visual/'
prefix1 = 'mmdetection/configs/'

algorithms = os.listdir(prefix+prefix1)

configs_list = []


html_content = ""



for algorithm in algorithms:
    configs = os.listdir(prefix + prefix1 +algorithm)

    for config in configs:
        if config.endswith('.svg'):
            configs_list.append(prefix + algorithm + '/' + config)
            csv_template = f'<a href="{prefix1+ algorithm +"/" + config}" target="_blank" rel="noopener noreferrer">{prefix1+ algorithm + config.replace(".svg", " 模型图")}</a><br>'
            html_content += csv_template + '\n'



with open('index.html', 'w') as f:
    f.write(html_content)