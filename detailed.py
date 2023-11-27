import requests
import re

def get_clan_members(api_key, clan_tag):
    url = f'https://api.clashofclans.com/v1/clans/{clan_tag}/members'

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Accept': 'application/json'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def get_player_info(api_key, player_tag):
    url = f'https://api.clashofclans.com/v1/players/{player_tag}'

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Accept': 'application/json'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def extract_number_from_name(name):
    match = re.search(r'\d+$', name)
    return int(match.group()) if match else 0

def convert_tag(tag):
    return tag.replace("#", "%23") if "#" in tag else "%23" + tag

def main(api_key, clan_tag):
    clan_members = get_clan_members(api_key, clan_tag)

    if clan_members:
        tarot_members = [member for member in clan_members['items'] if member['name'].startswith('塔罗牌')]
        sorted_tarot_members = sorted(tarot_members, key=lambda x: extract_number_from_name(x['name']))

        total_members = len(clan_members['items'])
        tarot_members_count = len(tarot_members)

        print(f"\n全部成员: {total_members}")
        print(f"塔罗牌成员数量: {tarot_members_count}")
        print("输出详细成员信息:")
        count = 0

        for member in sorted_tarot_members:
            member_tag = convert_tag(member['tag'])
            player_info = get_player_info(api_key, member_tag)

            if player_info:
                if player_info['townHallLevel'] >= 6:
                    count += 1
                print(f"{member['name']} ( {member['tag']} ), 大本营等级: {player_info['townHallLevel']}")
            else:
                print(f"无法获取玩家标签为 {tag} 的信息")

        print(f"高于6本的数量: {count}")

if __name__ == "__main__":
    # 请替换为你自己的API密钥和部落标签
    api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjRkOTY2Njc2LTUwZjMtNDEzZS1iZGFmLTQ5NjhjMDlkMWQyNSIsImlhdCI6MTcwMTA1MDExOSwic3ViIjoiZGV2ZWxvcGVyL2MzNGM2Zjc5LTMzM2EtOGQyMC1lZTBkLWJhNjA2OWJkNzYzNCIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjEwNC4yOC4yMTIuMTUwIl0sInR5cGUiOiJjbGllbnQifV19.UxhlaBi4U2NV3Jeh6PIfMj6BTAQ3XixCfKydCtZ7-aLDCDtOo47AFsqCi60iTYU8BuKO1c9uH4aEY96zE5OzrQ'
    clan_tag_input = input("输入部落标签: ").strip()
    clan_tag = convert_tag(clan_tag_input)

    main(api_key, clan_tag)
