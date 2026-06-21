import streamlit as st
import random

# ==========================================
# 1. 初始化暫存記憶體 (Session State)
# ==========================================
if 'player' not in st.session_state:
    st.session_state.player = {"學業": 0, "體力": 0, "存款": 0, "社交": 0}
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'week' not in st.session_state:
    st.session_state.week = 1
if 'ap' not in st.session_state:
    st.session_state.ap = 0
if 'credits' not in st.session_state:
    st.session_state.credits = 0
if 'event_message' not in st.session_state:
    st.session_state.event_message = ""
if 'pending_choice' not in st.session_state:
    st.session_state.pending_choice = None

# 新增機制變數
if 'skip_count' not in st.session_state:
    st.session_state.skip_count = 0  # 當週翹課次數
if 'prof_treat_count' not in st.session_state:
    st.session_state.prof_treat_count = 0  # 導生聚次數
if 'event_pool' not in st.session_state:
    st.session_state.event_pool = list(range(1, 18))  # 1 到 17 號選擇事件
if 'flag_67_friend' not in st.session_state:
    st.session_state.flag_67_friend = False
if 'flag_67_locked' not in st.session_state:
    st.session_state.flag_67_locked = False
if 'counters' not in st.session_state:
    st.session_state.counters = {
        "total_ap": 0, "read_ap": 0, "club_ap": 0, "work_ap": 0, "rest_ap": 0,
        "skips": 0, "exam_scores": []
    }

st.title("成功大學人生模擬器")

# ==========================================
# 2. 第 0 週：開局設定畫面
# ==========================================
if not st.session_state.game_started:
    st.header("第 0 週：學期初始設定")

    st.subheader("第一步：選擇學分")
    chosen_credits = st.slider("本學期修習學分數", 1, 30, 15)
    calculated_ap = 50 - chosen_credits
    st.info(f"預計每週行動點數 (AP)：50 - {chosen_credits} = **{calculated_ap}** 點")

    st.divider()

    st.subheader("第二步：設定初始天賦")
    tab1, tab2 = st.tabs(["🎲 隨機生成", "⚙️ 自訂分配"])

    with tab1:
        if st.button("隨機骰點並開始學期"):
            st.session_state.player["學業"] = random.randint(0, 40)
            st.session_state.player["體力"] = random.randint(0, 40)
            st.session_state.player["存款"] = random.randint(0, 40)
            st.session_state.player["社交"] = random.randint(0, 40)
            st.session_state.credits = chosen_credits
            st.session_state.ap = calculated_ap
            st.session_state.game_started = True
            st.rerun()

    with tab2:
        aca_pts = st.slider("學業", 0, 40, 20)
        hp_pts = st.slider("體力", 0, 40, 20)
        wealth_pts = st.slider("存款", 0, 40, 20)
        soc_pts = st.slider("社交", 0, 40, 20)

        if st.button("✅ 確認分配並開始學期"):
            st.session_state.player["學業"] = aca_pts
            st.session_state.player["體力"] = hp_pts
            st.session_state.player["存款"] = wealth_pts
            st.session_state.player["社交"] = soc_pts
            st.session_state.credits = chosen_credits
            st.session_state.ap = calculated_ap
            st.session_state.game_started = True
            st.rerun()

# ==========================================
# 3. 遊戲主畫面 (第 1 到 18 週)
# ==========================================
elif st.session_state.game_started and st.session_state.week <= 18:

    with st.sidebar:
        st.header("📊 角色狀態")
        st.write(f"**當前週次：** 第 {st.session_state.week} / 18 週")
        st.write(f"**本學期學分：** {st.session_state.credits}")

        st.divider()
        st.metric(label="📚 學業", value=st.session_state.player["學業"])
        st.metric(label="💪 體力", value=st.session_state.player["體力"])
        st.metric(label="💰 存款", value=st.session_state.player["存款"])
        st.metric(label="🤝 社交", value=st.session_state.player["社交"])

        st.divider()
        if st.button("重新開始遊戲"):
            st.session_state.clear()
            st.rerun()

    st.header(f"第 {st.session_state.week} 週：成大的日常")

    if st.session_state.event_message:
        st.warning(st.session_state.event_message)

    # ------------------------------------------
    # 3-A. 選擇事件處理區塊
    # ------------------------------------------
    if st.session_state.pending_choice is not None:
        c_id = st.session_state.pending_choice
        st.subheader("⚠️ 突發事件！請做出選擇")

        if c_id == 1:
            st.write("**【通識課遇到雷包組員】**期中報告大家都在裝死...")
            colA, colB = st.columns(2)
            if colA.button("自己全包 (學業+5, 體力-5, 社交-5)"):
                st.session_state.player["學業"] += 5
                st.session_state.player["體力"] -= 5
                st.session_state.player["社交"] -= 5
                st.session_state.event_message = "熬夜完成報告，分數保住了但身心俱疲。"
                st.session_state.pending_choice = None
                st.rerun()
            if colB.button("直接放推 (學業-5, 體力+5)"):
                st.session_state.player["學業"] -= 5
                st.session_state.player["體力"] += 5
                st.session_state.event_message = "大家一起拿零分，至少睡得很飽。"
                st.session_state.pending_choice = None
                st.rerun()

        elif c_id == 2:
            st.write("**【國華街排隊美食快閃】**知名甜點推出限量活動...")
            colA, colB = st.columns(2)
            if colA.button("翹課去排 (社交+5, 學業-3, 存款-5)"):
                st.session_state.player["社交"] += 5
                st.session_state.player["學業"] -= 3
                st.session_state.player["存款"] -= 5
                st.session_state.event_message = "發了限動朋友都很羨慕，但教授點名了。"
                st.session_state.pending_choice = None
                st.rerun()
            if colB.button("乖乖待在學校 (學業+2)"):
                st.session_state.player["學業"] += 2
                st.session_state.event_message = "不受誘惑專心聽課，剛好聽到考試重點。"
                st.session_state.pending_choice = None
                st.rerun()

        elif c_id == 3:
            st.write("**【系上活動急缺工人】**學長姐拜託幫忙搬東西佈置...")
            colA, colB = st.columns(2)
            if colA.button("義氣相挺 (社交+6, 體力-5)"):
                st.session_state.player["社交"] += 6
                st.session_state.player["體力"] -= 5
                st.session_state.event_message = "扛了超多重物，學長姐讚譽有加！"
                st.session_state.pending_choice = None
                st.rerun()
            if colB.button("裝死說沒空 (社交-3, 體力+3)"):
                st.session_state.player["社交"] -= 3
                st.session_state.player["體力"] += 3
                st.session_state.event_message = "回宿舍躺平，但在系上稍微黑掉了。"
                st.session_state.pending_choice = None
                st.rerun()

        elif c_id == 4:
            st.write("**【同學借錢修車】**同學機車拋錨急需 1000 元...")
            colA, colB = st.columns(2)
            if colA.button("借他 1000 元 (隨機結果)"):
                if random.random() < 0.7:
                    st.session_state.player["社交"] += 10
                    st.session_state.event_message = "隔天馬上還錢請喝星巴克！(存款無損,社交+10)"
                else:
                    st.session_state.player["存款"] -= 10
                    st.session_state.event_message = "同學搞消失，錢拿不回來了...(存款-10)"
                st.session_state.pending_choice = None
                st.rerun()
            if colB.button("委婉拒絕 (社交-2)"):
                st.session_state.player["社交"] -= 2
                st.session_state.event_message = "氣氛尷尬，但保住了存款。"
                st.session_state.pending_choice = None
                st.rerun()

        elif c_id == 5:
            st.write("**【在榕園撿到錢包】**地上有裝滿鈔票的錢包...")
            colA, colB = st.columns(2)
            if colA.button("送交生輔組 (學業+3, 體力-2)"):
                st.session_state.player["學業"] += 3
                st.session_state.player["體力"] -= 2
                st.session_state.event_message = "拾金不昧，處理手續花了點時間。"
                st.session_state.pending_choice = None
                st.rerun()
            if colB.button("當作沒看到 (無事發生)"):
                st.session_state.event_message = "快步離開現場。"
                st.session_state.pending_choice = None
                st.rerun()

        elif c_id == 6:
            st.write("**【選課系統當機】**明天加退選死線，系統網頁狂轉圈圈...")
            colA, colB = st.columns(2)
            if colA.button("狂按 F5 刷新 (隨機結果)"):
                if random.random() < 0.7:
                    st.session_state.player["學業"] += 5
                    st.session_state.player["體力"] -= 3
                    st.session_state.event_message = "順利搶到課！(學業+5, 體力-3)"
                else:
                    st.session_state.player["體力"] -= 5
                    st.session_state.event_message = "刷到半夜還是沒搶到。(體力-5)"
                st.session_state.pending_choice = None
                st.rerun()
            if colB.button("放棄去睡覺 (體力+5, 學業-3)"):
                st.session_state.player["體力"] += 5
                st.session_state.player["學業"] -= 3
                st.session_state.event_message = "隨緣選課，至少有睡飽。"
                st.session_state.pending_choice = None
                st.rerun()

        elif c_id == 7:
            st.write("**【系上期末聚餐】**群組揪團吃南紡高檔燒肉，預算有點緊...")
            colA, colB = st.columns(2)
            if colA.button("咬牙跟去吃 (存款-20, 社交+15, 體力+5)"):
                st.session_state.player["存款"] -= 20
                st.session_state.player["社交"] += 15
                st.session_state.player["體力"] += 5
                st.session_state.event_message = "大失血但跟大家打成一片吃很飽。"
                st.session_state.pending_choice = None
                st.rerun()
            if colB.button("找藉口不去 (社交-5)"):
                st.session_state.player["社交"] -= 5
                st.session_state.event_message = "省錢吃學餐，稍微有點脫節。"
                st.session_state.pending_choice = None
                st.rerun()

        elif c_id == 8:
            st.write("**【圖書館佔位亂象】**找位子看到空位上只放著一罐水...")
            colA, colB = st.columns(2)
            if colA.button("直接坐下去 (隨機結果)"):
                if random.random() < 0.5:
                    st.session_state.player["學業"] += 5
                    st.session_state.event_message = "對方沒回來，順利讀完書。(學業+5)"
                else:
                    st.session_state.player["社交"] -= 5
                    st.session_state.player["體力"] -= 5
                    st.session_state.event_message = "對方回來大吵一架，根本沒讀到書。(社交-5, 體力-5)"
                st.session_state.pending_choice = None
                st.rerun()
            if colB.button("摸摸鼻子換地方 (體力-2)"):
                st.session_state.player["體力"] -= 2
                st.session_state.event_message = "浪費力氣找新位子。"
                st.session_state.pending_choice = None
                st.rerun()

        elif c_id == 9:
            st.write("**【通識課的邂逅】**旁邊的同學長得完全是你的菜...")
            colA, colB = st.columns(2)
            if colA.button("勇敢搭訕 (隨機結果)"):
                if random.random() < 0.5:
                    st.session_state.player["社交"] += 8
                    st.session_state.player["體力"] += 5
                    st.session_state.event_message = "要到 IG 聊得很開心！(社交+8, 體力+5)"
                else:
                    st.session_state.player["體力"] -= 5
                    st.session_state.event_message = "被委婉拒絕，尷尬到爆。(體力-5)"
                st.session_state.pending_choice = None
                st.rerun()
            if colB.button("默默欣賞 (體力+2)"):
                st.session_state.player["體力"] += 2
                st.session_state.event_message = "心情愉悅但沒任何進展。"
                st.session_state.pending_choice = None
                st.rerun()

        elif c_id == 10:
            st.write("**【直屬的戀愛煩惱】**學姊半夜打來哭訴跟男友吵架...")
            colA, colB = st.columns(2)
            if colA.button("提供情緒價值 (社交+10, 存款+5, 體力-5)"):
                st.session_state.player["社交"] += 10
                st.session_state.player["存款"] += 5
                st.session_state.player["體力"] -= 5
                st.session_state.event_message = "聽她哭兩小時，隔天獲贈星巴克。"
                st.session_state.pending_choice = None
                st.rerun()
            if colB.button("找藉口想睡覺 (社交-5, 體力+5)"):
                st.session_state.player["社交"] -= 5
                st.session_state.player["體力"] += 5
                st.session_state.event_message = "明哲保身，獲得一夜好眠。"
                st.session_state.pending_choice = None
                st.rerun()

        elif c_id == 11:
            st.write("**【漁光島系沙烤】**下週系學會辦沙灘烤肉，報名費 500 元...")
            colA, colB = st.columns(2)
            if colA.button("繳錢參加 (存款-15, 社交+12, 體力-8)"):
                st.session_state.player["存款"] -= 15
                st.session_state.player["社交"] += 12
                st.session_state.player["體力"] -= 8
                st.session_state.event_message = "玩瘋了，滿身沙子超累。"
                st.session_state.pending_choice = None
                st.rerun()
            if colB.button("嫌麻煩不去 (體力+5, 社交-3)"):
                st.session_state.player["體力"] += 5
                st.session_state.player["社交"] -= 3
                st.session_state.event_message = "省錢省力，看大家發限動有點孤單。"
                st.session_state.pending_choice = None
                st.rerun()

        elif c_id == 12:
            st.write("**【週末夜唱大軍】**同學突然揪團賓士 KTV 夜唱到天亮...")
            colA, colB = st.columns(2)
            if colA.button("衝一波夜唱 (存款-10, 社交+10, 體力-12)"):
                st.session_state.player["存款"] -= 10
                st.session_state.player["社交"] += 10
                st.session_state.player["體力"] -= 12
                st.session_state.event_message = "唱到失聲，隔天直接睡死。"
                st.session_state.pending_choice = None
                st.rerun()
            if colB.button("拒絕保肝 (體力+8, 社交-2)"):
                st.session_state.player["體力"] += 8
                st.session_state.player["社交"] -= 2
                st.session_state.event_message = "堅定拒絕誘惑。"
                st.session_state.pending_choice = None
                st.rerun()

        elif c_id == 13:
            st.write("**【同溫層的誘惑】**朋友瘋狂「67」打混摸魚，約你翹課打咖...")
            colA, colB = st.columns(2)
            if colA.button("一起 67！ (學業-5, 社交+8, 體力+5)"):
                st.session_state.player["學業"] -= 5
                st.session_state.player["社交"] += 8
                st.session_state.player["體力"] += 5
                st.session_state.flag_67_friend = True
                st.session_state.event_message = "快樂就是這麼簡單。"
                st.session_state.pending_choice = None
                st.rerun()
            if colB.button("打心底看不起他們 (學業+5, 社交-5)"):
                st.session_state.player["學業"] += 5
                st.session_state.player["社交"] -= 5
                st.session_state.event_message = "獨自去上課，覺得自己是清流。"
                st.session_state.pending_choice = None
                st.rerun()

        elif c_id == 14:
            st.write("**【TWICE 台灣演唱會】**搶票日大戰...")
            colA, colB = st.columns(2)
            if colA.button("跟著搶票 (隨機結果)"):
                rnd = random.random()
                if rnd < 0.3:
                    st.session_state.player["存款"] -= 30
                    st.session_state.player["體力"] += 20
                    st.session_state.event_message = "搶到神席！心靈大滿足。(存款-30,體力+20)"
                elif st.session_state.player["社交"] > 25:
                    st.session_state.player["存款"] -= 30
                    st.session_state.player["社交"] += 5
                    st.session_state.player["體力"] += 15
                    st.session_state.event_message = "沒搶到，但朋友讓票給你！(存款-30,社交+5,體力+15)"
                else:
                    st.session_state.player["體力"] -= 5
                    st.session_state.event_message = "沒搶到，白白浪費時間。(體力-5)"
                st.session_state.pending_choice = None
                st.rerun()
            if colB.button("讓給真粉 (無事發生)"):
                st.session_state.event_message = "不參與這場戰爭。"
                st.session_state.pending_choice = None
                st.rerun()

        elif c_id == 15:
            st.write("**【期末的誘惑】**高中同學跑來台南找你玩...")
            colA, colB = st.columns(2)
            if colA.button("讀期末考 (學業+8, 社交-5)"):
                st.session_state.player["學業"] += 8
                st.session_state.player["社交"] -= 5
                st.session_state.event_message = "忍痛拒絕，專注課業。"
                st.session_state.pending_choice = None
                st.rerun()
            if colB.button("帶他吃遍台南 (社交+10, 學業-8, 存款-15, 體力-10)"):
                st.session_state.player["社交"] += 10
                st.session_state.player["學業"] -= 8
                st.session_state.player["存款"] -= 15
                st.session_state.player["體力"] -= 10
                st.session_state.event_message = "盡地主之誼，荷包跟成績大失血。"
                st.session_state.pending_choice = None
                st.rerun()

        elif c_id == 16:
            st.write("**【系卡 K 大賽】**系上舉辦歌唱比賽，大家都在起鬨...")
            colA, colB = st.columns(2)
            if colA.button("在台下看表演 (體力+2, 社交+2)"):
                st.session_state.player["體力"] += 2
                st.session_state.player["社交"] += 2
                st.session_state.event_message = "當個安靜的觀眾。"
                st.session_state.pending_choice = None
                st.rerun()
            if colB.button("上台秀一曲 (社交+8, 體力-3)"):
                st.session_state.player["社交"] += 8
                st.session_state.player["體力"] -= 3
                st.session_state.event_message = "五音不全引發爆笑，稍微丟臉但炒熱氣氛。"
                st.session_state.pending_choice = None
                st.rerun()

        elif c_id == 17:
            st.write("**【麥當勞鬆餅堡之亂】**期間限定厚鬆餅堡排隊人潮爆滿...")
            colA, colB = st.columns(2)
            if colA.button("排隊嚐鮮 (存款-5, 隨機結果)"):
                st.session_state.player["存款"] -= 5
                if random.random() < 0.5:
                    st.session_state.player["體力"] += 10
                    st.session_state.event_message = "甜鹹口感超讚！(體力+10)"
                else:
                    st.session_state.player["體力"] -= 5
                    st.session_state.event_message = "根本邪教組合，越吃越生氣。(體力-5)"
                st.session_state.pending_choice = None
                st.rerun()
            if colB.button("不湊熱鬧 (無事發生)"):
                st.session_state.event_message = "省下時間與金錢。"
                st.session_state.pending_choice = None
                st.rerun()

        elif c_id == 18:
            st.write("**【67 的真諦】**朋友似乎參透了 67 的真諦，轉頭看向你。")
            colA, colB = st.columns(2)
            if colA.button("67") or colB.button("67 "):
                st.session_state.flag_67_locked = True
                st.session_state.player = {"學業": 67, "體力": 67, "存款": 67, "社交": 67}
                st.session_state.event_message = "一切都變成了 67。"
                st.session_state.pending_choice = None
                st.rerun()

    # ------------------------------------------
    # 3-B. 資源分配區塊
    # ------------------------------------------
    else:
        st.write(f"本週可用 AP：**{st.session_state.ap}**")

        can_skip = st.session_state.skip_count < st.session_state.credits
        if can_skip:
            n = st.session_state.skip_count + 1
            penalty = int(1 + (n * (n - 1)) / 2)
            if st.button(f"🙈 選擇翹課 (獲得 3 AP，學業 -{penalty})"):
                if st.session_state.ap < 50:
                    st.session_state.skip_count += 1
                    st.session_state.counters["skips"] += 1
                    st.session_state.player["學業"] -= penalty
                    st.session_state.ap = min(50, st.session_state.ap + 3)
                    st.rerun()
                else:
                    st.warning("AP 已達上限 (50)。")

        st.divider()
        st.write("分配本週的行程（剩餘 AP 自動轉為休息恢復體力）：")
        read_ap = st.slider("📚 讀書投入", 0, st.session_state.ap, 0)
        club_ap = st.slider("🎸 社團投入", 0, st.session_state.ap, 0)
        work_ap = st.slider("💼 打工投入", 0, st.session_state.ap, 0)

        total_alloc = read_ap + club_ap + work_ap
        rest_ap = st.session_state.ap - total_alloc

        if total_alloc > st.session_state.ap:
            st.error(f"分配總和超出可用 AP ({total_alloc} / {st.session_state.ap})，請調低！")
        else:
            st.info(f"將有 {rest_ap} 點 AP 轉換為休息時間。")
            if st.button("確認分配並進入下一週"):
                # 更新屬性
                st.session_state.player["學業"] += int(read_ap * 1.2)
                st.session_state.player["體力"] -= int(read_ap * 0.5)

                st.session_state.player["社交"] += int(club_ap * 1.0)
                st.session_state.player["存款"] -= int(club_ap * 0.5)
                st.session_state.player["體力"] -= int(club_ap * 0.8)

                st.session_state.player["存款"] += int(work_ap * 1.5)
                st.session_state.player["體力"] -= int(work_ap * 0.8)

                st.session_state.player["體力"] += int(rest_ap * 1.5)

                # 更新計數器
                st.session_state.counters["total_ap"] += st.session_state.ap
                st.session_state.counters["read_ap"] += read_ap
                st.session_state.counters["club_ap"] += club_ap
                st.session_state.counters["work_ap"] += work_ap
                st.session_state.counters["rest_ap"] += rest_ap

                msg_list = []

                # 負面狀態檢定
                if not st.session_state.flag_67_locked:
                    if st.session_state.player["體力"] < 15:
                        penalty_ap = int((50 - st.session_state.credits) * 0.3)
                        st.session_state.ap = max(0, (50 - st.session_state.credits) - penalty_ap)
                        msg_list.append(f"💀 【免疫力崩潰】體力過低，下週減少 {penalty_ap} 點 AP。")
                    else:
                        st.session_state.ap = 50 - st.session_state.credits

                    if st.session_state.player["存款"] < 15:
                        st.session_state.player["體力"] -= 3
                        msg_list.append("💀 【月底吃土】存款過低只能吃泡麵，體力下降。")

                    if st.session_state.player["社交"] < 15:
                        st.session_state.player["學業"] -= 3
                        msg_list.append("💀 【邊緣人危機】錯過情報，學業下降。")
                else:
                    st.session_state.ap = 50 - st.session_state.credits

                # 時間固定事件與考試
                if st.session_state.week in [8, 17] and not st.session_state.flag_67_locked:
                    st.session_state.player["學業"] += 5
                    msg_list.append("📝 【助教洩題】考前拿到重點筆記，學業提升！")

                if st.session_state.week in [9, 18]:
                    score = st.session_state.player["學業"] + random.randint(-10, 10)
                    if st.session_state.flag_67_locked:
                        score = 67
                    score = max(0, min(100, int(score)))
                    st.session_state.counters["exam_scores"].append(score)
                    msg_list.append(f"💯 【考試結束】你的表現評分為：{score}。")

                # 隨機抽取事件 (70% 機率)
                if not st.session_state.flag_67_locked and random.random() < 0.70:
                    if st.session_state.flag_67_friend and random.random() < 0.02:
                        st.session_state.pending_choice = 18
                    else:
                        if random.random() < 0.5 and len(st.session_state.event_pool) > 0:
                            idx = random.randint(0, len(st.session_state.event_pool) - 1)
                            picked = st.session_state.event_pool.pop(idx)
                            # 確保事件 15 只在 16-18 週發生
                            if picked == 15 and st.session_state.week < 16:
                                st.session_state.event_pool.append(15)
                                rand_ev = random.randint(1, 15)
                                # 備用隨機事件處理
                                if rand_ev == 1:
                                    st.session_state.player["存款"] += 6
                                    msg_list.append("🔔 發票中獎獲得 600 元！")
                            else:
                                st.session_state.pending_choice = picked
                        elif st.session_state.pending_choice is None:
                            rand_ev = random.randint(1, 15)
                            if rand_ev == 1:
                                money = random.choice([2, 6, 10])
                                st.session_state.player["存款"] += money
                                msg_list.append(f"🔔 發票中獎獲得 {money}00 元！")
                            elif rand_ev == 2:
                                st.session_state.player["體力"] -= 5
                                st.session_state.ap = max(0, st.session_state.ap - 10)
                                msg_list.append("🔔 台南太熱導致中暑！(體力-5, AP-10)")
                            elif rand_ev == 3:
                                st.session_state.player["體力"] += 3
                                st.session_state.player["社交"] += 3
                                msg_list.append("🔔 學長姐請客吃直屬聚！(體力+3, 社交+3)")
                            elif rand_ev == 4:
                                st.session_state.player["存款"] -= 10
                                msg_list.append("🔔 機車違停被拖吊了...(存款-10)")
                            elif rand_ev == 5:
                                st.session_state.player["存款"] -= 15
                                msg_list.append("🔔 腳踏車被偷了！(存款-15)")
                            elif rand_ev == 6:
                                if st.session_state.prof_treat_count < 2:
                                    st.session_state.player["體力"] += 5
                                    st.session_state.player["社交"] += 5
                                    st.session_state.player["學業"] += 2
                                    st.session_state.prof_treat_count += 1
                                    msg_list.append("🔔 教授請客吃導生聚！")
                                else:
                                    st.session_state.player["存款"] += 5
                                    msg_list.append("🔔 走在路上撿到 500 塊！")
                            elif rand_ev == 7:
                                st.session_state.player["學業"] += 5
                                st.session_state.player["體力"] += 3
                                msg_list.append("🔔 通識課遇到神仙組員！(學業+5, 體力+3)")
                            elif rand_ev == 8:
                                st.session_state.player["存款"] += 20
                                msg_list.append("🔔 申請的補助入帳了！(存款+20)")
                            elif rand_ev == 9:
                                st.session_state.player["學業"] -= 5
                                st.session_state.player["體力"] -= 3
                                msg_list.append("🔔 死線前筆電當機...(學業-5, 體力-3)")
                            elif rand_ev == 10:
                                st.session_state.player["存款"] -= 8
                                st.session_state.player["體力"] -= 5
                                msg_list.append("🔔 光復校區腳踏車犁田！(存款-8, 體力-5)")
                            elif rand_ev == 11:
                                st.session_state.player["學業"] -= 3
                                st.session_state.player["體力"] -= 2
                                msg_list.append("🔔 小東路地下道淹水遲到。(學業-3, 體力-2)")
                            elif rand_ev == 12:
                                st.session_state.player["體力"] += 5
                                st.session_state.player["存款"] -= 3
                                msg_list.append("🔔 買到勝利早點最後一份！(體力+5, 存款-3)")
                            elif rand_ev == 13:
                                st.session_state.player["體力"] -= 8
                                msg_list.append("🔔 體育課操場測驗，快虛脫。(體力-8)")
                            elif rand_ev == 14:
                                st.session_state.player["學業"] += 5
                                st.session_state.player["體力"] += 3
                                msg_list.append("🔔 發現不點名涼課！(學業+5, 體力+3)")
                            elif rand_ev == 15:
                                st.session_state.player["存款"] -= 5
                                st.session_state.player["社交"] -= 3
                                msg_list.append("🔔 遇到火車站前愛心筆推銷。(存款-5, 社交-3)")

                # 防止數值小於 0 (67狀態不受限)
                if not st.session_state.flag_67_locked:
                    for k in st.session_state.player:
                        st.session_state.player[k] = max(0, int(st.session_state.player[k]))
                else:
                    st.session_state.player = {"學業": 67, "體力": 67, "存款": 67, "社交": 67}

                st.session_state.skip_count = 0
                st.session_state.week += 1
                st.session_state.event_message = "\n\n".join(msg_list) if msg_list else "本週平安無事地過去了。"
                st.rerun()

# ==========================================
# 4. 結局結算畫面
# ==========================================
elif st.session_state.game_started and st.session_state.week > 18:
    st.header("🎓 遊戲結束！成大生活結算")

    f_aca = st.session_state.player["學業"]
    f_hp = st.session_state.player["體力"]
    f_wlt = st.session_state.player["存款"]
    f_soc = st.session_state.player["社交"]

    st.subheader("最終狀態")
    st.write(f"📚 學業：{f_aca} | 💪 體力：{f_hp} | 💰 存款：{f_wlt} | 🤝 社交：{f_soc}")

    st.divider()

    # 統計資料與成就
    c = st.session_state.counters
    t_ap = max(1, c["total_ap"])  # 避免除以零
    p_rd = c["read_ap"] / t_ap
    p_wk = c["work_ap"] / t_ap
    p_cl = c["club_ap"] / t_ap
    p_rs = c["rest_ap"] / t_ap

    st.subheader("📊 學期數據總覽")
    st.write(f"總翹課次數：{c['skips']} 次")
    st.write(f"時間分配：讀書 {p_rd:.0%} | 打工 {p_wk:.0%} | 社團 {p_cl:.0%} | 休息 {p_rs:.0%}")
    if len(c["exam_scores"]) == 2:
        st.write(f"考試成績：期中 {c['exam_scores'][0]} 分 | 期末 {c['exam_scores'][1]} 分")

    achievements = []
    # 翹課系列
    if c["skips"] == 0: achievements.append("🏅【全勤好寶寶】")
    if c["skips"] > 10: achievements.append("🏅【我有自己的節奏】")
    if c["skips"] > 20: achievements.append("🏅【教授：查無此人】")
    if c["skips"] > 50: achievements.append("🏅【要不這個學咱就不上了】")

    # 時間系列
    if p_rd > 0.75:
        achievements.append("🏅【卷王就是你】")
    elif p_rd > 0.5:
        achievements.append("🏅【認真讀書好寶寶】")
    if p_wk > 0.75:
        achievements.append("🏅【打工魔人】")
    elif p_wk > 0.5:
        achievements.append("🏅【校園打工仔】")
    if p_cl > 0.75:
        achievements.append("🏅【活動長好！】")
    elif p_cl > 0.5:
        achievements.append("🏅【活動狂人】")
    if p_rs > 0.5: achievements.append("🏅【成大卡比獸】")
    if 0.25 <= p_rd <= 0.35 and 0.25 <= p_wk <= 0.35 and 0.25 <= p_cl <= 0.35:
        achievements.append("🏅【時間管理大師】")

    # 考試系列
    if len(c["exam_scores"]) == 2:
        if c["exam_scores"][0] > 95 and c["exam_scores"][1] > 95:
            achievements.append("🏅【學神降臨】")
        if (c["exam_scores"][0] + c["exam_scores"][1]) / 2 == 60:
            achievements.append("🏅【生死一瞬間】")
        if (c["exam_scores"][0] + c["exam_scores"][1]) / 2 < 30:
            achievements.append("🏅【這題超出了我的認知】")

    if achievements:
        st.subheader("🏆 獲得成就")
        for ach in achievements:
            st.write(ach)

    st.divider()
    st.subheader("🌟 你的專屬結局")

    if st.session_state.flag_67_locked:
        st.success("【67676767】你參透了宇宙的真理，這學期圓滿了。")
    elif f_aca >= 150 and f_hp < 20:
        st.success("【爆肝學霸】拿到了書卷獎，但身體快扛不住啦！")
    elif f_soc >= 150:
        st.success("【公關達人】走到育樂街都有認識的攤販老闆，台南簡直是你的主場！")
    elif f_wlt >= 150:
        st.success("【學生富豪】打工賺得比正職還多，學分什麼的就當作交朋友吧！")
    elif f_aca < 30:
        st.error("【延畢大師】這學期的學分岌岌可危，準備多留一年吃丹丹漢堡了...")
    else:
        st.info("【平凡大學生】平安順利度過了充實的一學期，穩穩當當也是一種幸福！")

    st.divider()
    if st.button("🔄 重新開始大學生活"):
        st.session_state.clear()
        st.rerun()