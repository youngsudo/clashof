import requests
import tkinter as tk
from tkinter import ttk
import re

def get_clan_members(api_key, clan_tag):
    url = f'https://api.clashofclans.com/v1/clans/{clan_tag}/members'

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Accept': 'application/json'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def extract_number_from_name(name):
    match = re.search(r'\d+$', name)
    return int(match.group()) if match else 0

def on_submit():
    clan_tag_input = clan_tag_entry.get().strip() 

    # 检查用户是否输入了部落标签
    if not clan_tag_input:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "请输入标签.")
        return

    clan_tag = ""
    if "#" in clan_tag_input:
        clan_tag = clan_tag_input.replace("#", "%23")
    else:
        clan_tag = "%23" + clan_tag_input

    clan_members = get_clan_members(api_key, clan_tag)

    if clan_members:
        tarot_members = [member for member in clan_members['items'] if member['name'].startswith('塔罗牌')]
        sorted_tarot_members = sorted(tarot_members, key=lambda x: extract_number_from_name(x['name']))

        # 清空之前的结果
        result_text.delete(1.0, tk.END)

        # 写入排序后的结果到文本框
        result_text.insert(tk.END, "排序:\n")
        for member in sorted_tarot_members:
            result_text.insert(tk.END, f"- {member['name']}\n")

        # 输出符合条件的数量和全部数量
        total_members = len(clan_members['items'])
        tarot_members_count = len(tarot_members)
        result_text.insert(tk.END, f"\n成员总数: {total_members}\n")
        result_text.insert(tk.END, f"塔罗牌成员数: {tarot_members_count}")
    else:
        # 输出错误信息到文本框
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "查询失败，请检查标签和API密钥。")


# 请替换为你自己的API密钥
api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjRkOTY2Njc2LTUwZjMtNDEzZS1iZGFmLTQ5NjhjMDlkMWQyNSIsImlhdCI6MTcwMTA1MDExOSwic3ViIjoiZGV2ZWxvcGVyL2MzNGM2Zjc5LTMzM2EtOGQyMC1lZTBkLWJhNjA2OWJkNzYzNCIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjEwNC4yOC4yMTIuMTUwIl0sInR5cGUiOiJjbGllbnQifV19.UxhlaBi4U2NV3Jeh6PIfMj6BTAQ3XixCfKydCtZ7-aLDCDtOo47AFsqCi60iTYU8BuKO1c9uH4aEY96zE5OzrQ'


# 创建主窗口
root = tk.Tk()
root.title("查询塔罗牌")

# 创建标签和输入框
clan_tag_label = ttk.Label(root, text="输入标签:")
clan_tag_label.grid(row=0, column=0, padx=10, pady=10)

clan_tag_entry = ttk.Entry(root)
clan_tag_entry.grid(row=0, column=1, padx=10, pady=10)

# 创建按钮
submit_button = ttk.Button(root, text="确定", command=on_submit)
submit_button.grid(row=1, column=0, columnspan=2, pady=10)

# 创建文本框用于显示结果
result_text = tk.Text(root, height=30, width=50)
result_text.grid(row=2, column=0, columnspan=2, pady=10)

# 运行主循环
root.mainloop()