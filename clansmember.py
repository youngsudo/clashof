# 查询塔罗牌部落成员信息
#2G9CPR2LY（总部）大阿卡纳22
#2QQQPYYPY  （1部) 小阿卡纳40 权仗、圣杯、宝剑、星币
#2QQQ99YVQ （2部）序列1-50
#2QQQ99ULV （3部）序列51-100
import requests
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

def main():
    # 请替换为你自己的API密钥和部落标签
    api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjRkOTY2Njc2LTUwZjMtNDEzZS1iZGFmLTQ5NjhjMDlkMWQyNSIsImlhdCI6MTcwMTA1MDExOSwic3ViIjoiZGV2ZWxvcGVyL2MzNGM2Zjc5LTMzM2EtOGQyMC1lZTBkLWJhNjA2OWJkNzYzNCIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjEwNC4yOC4yMTIuMTUwIl0sInR5cGUiOiJjbGllbnQifV19.UxhlaBi4U2NV3Jeh6PIfMj6BTAQ3XixCfKydCtZ7-aLDCDtOo47AFsqCi60iTYU8BuKO1c9uH4aEY96zE5OzrQ'
    # clan_tag = '%232G9CPR2LY'  # 注意：氏族标签中的#需要被替换为%23
    clan_tag_input = input("Enter Clan Tag: ")
    # clan_tag = clan_tag_input if "#" in clan_tag_input else "%23" + clan_tag_input
    clan_tag = ""
    if "#" in clan_tag_input:
        clan_tag = clan_tag_input.replace("#", "%23")
    else:
        clan_tag = "%23" + clan_tag_input

    clan_members = get_clan_members(api_key, clan_tag)

    """ 
        打印全部成员信息
        # if clan_members:
        #     print("Clan Members:")
        #     for member in clan_members['items']:
        #         print(f"- {member['name']} ({member['role']})")
    """

    # 提取以"塔罗牌"开头的成员信息
    tarot_members = [member for member in clan_members['items'] if member['name'].startswith('塔罗牌')]
    leader = [member for member in clan_members['items'] if member['role']=="leader"]
    # 按成员名称中的数字进行排序
    sorted_tarot_members = sorted(tarot_members, key=lambda x: extract_number_from_name(x['name']))

    # 打印排序后的结果
    print(f"首领: {leader[0]['name']}")
    print("Sorted Tarot Members:")
    for member in sorted_tarot_members:
        print(f"- {member['name']}")

    # 输出符合条件的数量和全部数量
    total_members = len(clan_members['items'])
    tarot_members_count = len(tarot_members)
    print(f"\n全部成员: {total_members}")
    print(f"塔罗牌成员员数量: {tarot_members_count}")

if __name__ == "__main__":
    main()
