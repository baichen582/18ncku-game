import streamlit as st
import random

# ==========================================
# 1. 初始化暫存記憶體 (Session State)
# ==========================================
if 'player' not in st.session_state:
    st.session_state.player = {"學業": 0, "健康": 0, "存款": 0, "社交": 0}
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
if 'skip_count' not in st.session_state:
    st.session_state.skip_count = 0  # 紀錄當週翹課次數
if 'prof_treat_count' not in st.session_state:
    st.session_state.prof_treat_count = 0  # 紀錄導生聚次數
if 'pending_choice' not in st.session_state:
    st.session_state.pending_choice = None  # 紀錄等待玩家選擇的事件 ID

st.title("成功大學人生模擬器")

# ==========================================
# 2. 第 0 週：開局設定畫面
# ==========================================
if not st.session_state.game_started:
    st.header("第 0 週：學期初始設定")

    st.subheader("第一步：選擇學分")
    st.write("學分越重，每週可自由支配的行動點數（AP）就越少。")
    chosen_credits = st.slider("本學期修習學分數", 1, 30, 15)
    calculated_ap = 50 - chosen_credits
    st.info(f"預計每週行動點數 (AP)：50 - {chosen_credits} = **{calculated_ap}** 點")

    st.divider()

    st.subheader("第二步：設定初始天賦")
    st.write("調整你的初始狀態 (0~40)，打造專屬的開局條件。")
    aca_pts = st.slider("學業", 0, 40, 20)
    hp_pts = st.slider("健康", 0, 40, 20)
    wealth_pts = st.slider("存款", 0, 40, 20)
    soc_pts = st.slider("社交", 0, 40, 20)

    if st.button("✅ 確認分配並開始學期"):
        st.session_state.player["學業"] = aca_pts
        st.session_state.player["健康"] = hp_pts
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

    # 側邊欄狀態列
    with st.sidebar:
        st.header("📊 角色狀態")
        st.write(f"**當前週次：** 第 {st.session_state.week} / 18 週")
        st.write(f"**本學期學分：** {st.session_state.credits}")
        st.write(f"**剩餘 AP：** {st.session_state.ap}")

        st.divider()
        st.metric(label="📚 學業", value=st.session_state.player["學業"])
        st.metric(label="💪 健康", value=st.session_state.player["健康"])
        st.metric(label="💰 存款", value=st.session_state.player["存款"])
        st.metric(label="🤝 社交", value=st.session_state.player["社交"])

        st.divider()
        if st.button("重新開始遊戲"):
            st.session_state.clear()
            st.rerun()

    st.header(f"第 {st.session_state.week} 週：成大的日常")

    # 顯示上週結算或當前發生的事件訊息
    if st.session_state.event_message:
        st.warning(st.session_state.event_message)

    # ------------------------------------------
    # 3-A. 選擇事件處理區塊 (若有未決定的事件則鎖定其他行動)
    # ------------------------------------------
    if st.session_state.pending_choice is not None:
        choice_id = st.session_state.pending_choice
        st.subheader("⚠️ 突發事件！請做出選擇")

        if choice_id == 1:
            st.write("**【通識課遇到雷包組員】**期中報告大家都在裝死，死線快到了...")
            colA, colB = st.columns(2)
            if colA.button("自己全包 (學業+5, 健康-5, 社交-5)"):
                st.session_state.player["學業"] += 5
                st.session_state.player["健康"] -= 5
                st.session_state.player["社交"] -= 5
                st.session_state.event_message = "你熬夜完成了報告，分數保住了，但身心俱疲且對人性感到失望。"
                st.session_state.pending_choice = None
                st.rerun()
            if colB.button("直接放推 (學業-5, 健康+5)"):
                st.session_state.player["學業"] -= 5
                st.session_state.player["健康"] += 5
                st.session_state.event_message = "大家一起拿零分，至少你睡得很飽。"
                st.session_state.pending_choice = None
                st.rerun()

        elif choice_id == 2:
            st.write("**【國華街排隊美食快閃】**知名甜點推出限量活動，但卡到必修課...")
            colA, colB = st.columns(2)
            if colA.button("翹課去排 (社交+5, 學業-3, 存款-5)"):
                st.session_state.player["社交"] += 5
                st.session_state.player["學業"] -= 3
                st.session_state.player["存款"] -= 5
                st.session_state.event_message = "你買到限量甜點並發了限動，朋友們都很羨慕，但教授點名了。"
                st.session_state.pending_choice = None
                st.rerun()
            if colB.button("乖乖待在學校 (學業+2)"):
                st.session_state.player["學業"] += 2
                st.session_state.event_message = "你不受誘惑專心聽課，這堂課的內容剛好是考試重點。"
                st.session_state.pending_choice = None
                st.rerun()

        elif choice_id == 3:
            st.write("**【系上活動急缺工人】**學長姐跑來拜託你幫忙搬東西佈置...")
            colA, colB = st.columns(2)
            if colA.button("義氣相挺 (社交+6, 健康-3, 當週AP-5)"):
                st.session_state.player["社交"] += 6
                st.session_state.player["健康"] -= 3
                st.session_state.ap -= 5
                st.session_state.event_message = "你幫忙扛了超多重物，學長姐對你讚譽有加！"
                st.session_state.pending_choice = None
                st.rerun()
            if colB.button("裝死說沒空 (社交-3, 健康+3)"):
                st.session_state.player["社交"] -= 3
                st.session_state.player["健康"] += 3
                st.session_state.event_message = "你選擇明哲保身回宿舍躺平，但在系上稍微黑掉了。"
                st.session_state.pending_choice = None
                st.rerun()

        elif choice_id == 4:
            st.write("**【同學借錢修車】**同學的機車在路上拋錨，急需借 1000 元...")
            colA, colB = st.columns(2)
            if colA.button("借他 1000 元 (存款-10，後續隨機)"):
                if random.random() < 0.7:
                    st.session_state.player["社交"] += 10
                    st.session_state.event_message = "他隔天馬上還錢，還請你喝了一杯星巴克！(存款無損，社交大增)"
                else:
                    st.session_state.player["存款"] -= 10
                    st.session_state.event_message = "結果他開始搞消失，你的錢拿不回來了...(存款-10)"
                st.session_state.pending_choice = None
                st.rerun()
            if colB.button("委婉拒絕 (社交-2)"):
                st.session_state.player["社交"] -= 2
                st.session_state.event_message = "你表示自己手頭也很緊，氣氛稍微有些尷尬。"
                st.session_state.pending_choice = None
                st.rerun()

        elif choice_id == 5:
            st.write("**【在榕園撿到錢包】**地上有一個裝滿千元大鈔的錢包...")
            colA, colB = st.columns(2)
            if colA.button("送交生輔組 (學業/道德+3, AP-3)"):
                st.session_state.player["學業"] += 3
                st.session_state.ap -= 3
                st.session_state.event_message = "拾金不昧！處理手續花了點時間，但感覺做了件好事。"
                st.session_state.pending_choice = None
                st.rerun()
            if colB.button("當作沒看到 (無事發生)"):
                st.session_state.event_message = "你選擇不惹麻煩，快步離開現場。"
                st.session_state.pending_choice = None
                st.rerun()

    # ------------------------------------------
    # 3-B. 一般行動分配區塊 (沒有突發事件時顯示)
    # ------------------------------------------
    else:
        st.write(f"本週剩餘 AP：**{st.session_state.ap}**")

        # 考前崩潰期判定
        is_exam_prep = st.session_state.week in [5, 14]
        study_ap_cost = 15 if is_exam_prep else 10
        if is_exam_prep:
            st.info("🚨 考前崩潰期：圖書館與咖啡廳爆滿，讀書選項需消耗更多 AP！")

        # 翹課系統
        st.subheader("⚠️ 高風險行動")
        can_skip = st.session_state.skip_count < st.session_state.credits
        if can_skip:
            # 遞增扣分公式：n=1扣1, n=2扣2, n=3扣4, n=4扣7 -> 1 + (n * (n - 1)) / 2
            n = st.session_state.skip_count + 1
            penalty = int(1 + (n * (n - 1)) / 2)

            if st.button(f"🙈 選擇翹課 (獲得 3 AP，學業 -{penalty})"):
                if st.session_state.ap < 50:
                    st.session_state.skip_count += 1
                    st.session_state.player["學業"] -= penalty
                    st.session_state.ap = min(50, st.session_state.ap + 3)
                    st.rerun()
                else:
                    st.warning("AP 已達上限 (50)，無法再翹課獲取！")
        else:
            st.write("本週翹課額度已達學分上限，乖乖去上課吧！")

        st.divider()
        st.subheader("日常行動")

        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"📚 圖書館讀書 (-{study_ap_cost} AP)"):
                if st.session_state.ap >= study_ap_cost:
                    st.session_state.ap -= study_ap_cost
                    st.session_state.player["學業"] += random.randint(3, 5)
                    st.session_state.player["健康"] -= random.randint(1, 3)
                    st.rerun()
                else:
                    st.warning("AP 不足！")

            if st.button(f"☕ 咖啡廳讀書 (-{study_ap_cost} AP)"):
                if st.session_state.ap >= study_ap_cost:
                    st.session_state.ap -= study_ap_cost
                    st.session_state.player["學業"] += random.randint(2, 4)
                    st.session_state.player["健康"] -= 1
                    st.session_state.player["存款"] -= random.randint(2, 4)
                    st.rerun()
                else:
                    st.warning("AP 不足！")

            if st.button("🗣️ 讀書會 (-12 AP)"):
                if st.session_state.ap >= 12:
                    st.session_state.ap -= 12
                    st.session_state.player["學業"] += random.randint(4, 6)
                    st.session_state.player["健康"] -= random.randint(2, 4)
                    st.session_state.player["社交"] += random.randint(2, 4)
                    st.rerun()
                else:
                    st.warning("AP 不足！")

        with col2:
            if st.button("🛏️ 宿舍休息 (-10 AP)"):
                if st.session_state.ap >= 10:
                    st.session_state.ap -= 10
                    st.session_state.player["健康"] += random.randint(6, 10)
                    st.rerun()
                else:
                    st.warning("AP 不足！")

        st.divider()
        st.subheader("社團與打工 (自由分配 AP)")

        club_ap = st.slider("選擇投入社團的 AP", 1, max(1, st.session_state.ap), 5)
        if st.button(f"🎸 參加社團 (消耗 {club_ap} AP)"):
            if st.session_state.ap >= club_ap:
                st.session_state.ap -= club_ap
                st.session_state.player["社交"] += int(club_ap * 0.8)
                st.session_state.player["存款"] -= int(club_ap * 0.4)
                # 健康隨機增減 (-50% 到 +50% 的投入值)
                hp_change = random.randint(int(-club_ap * 0.5), int(club_ap * 0.5))
                st.session_state.player["健康"] += hp_change
                st.rerun()
            else:
                st.warning("AP 不足！")

        job_ap = st.slider("選擇打工排班的 AP", 5, 25, 10)
        if st.button(f"💼 打工賺錢 (消耗 {job_ap} AP)"):
            if st.session_state.ap >= job_ap:
                st.session_state.ap -= job_ap
                st.session_state.player["存款"] += int(job_ap * 1.5)
                st.session_state.player["健康"] -= int(job_ap * 0.6)
                st.rerun()
            else:
                st.warning("AP 不足！")

        st.divider()

        # ------------------------------------------
        # 3-C. 換週與事件結算引擎
        # ------------------------------------------
        if st.button("➡️ 結束本週，進入下一週"):
            msg_list = []

            # 結算負面狀態
            if st.session_state.player["健康"] < 15:
                penalty_ap = int((50 - st.session_state.credits) * 0.3)
                st.session_state.ap = max(0, (50 - st.session_state.credits) - penalty_ap)
                msg_list.append(f"💀 【免疫力崩潰】健康過低，下週減少 {penalty_ap} 點 AP。")
            else:
                st.session_state.ap = 50 - st.session_state.credits

            if st.session_state.player["存款"] < 15:
                st.session_state.player["健康"] -= 3
                msg_list.append("💀 【月底吃土】存款過低只能吃泡麵，健康下降。")

            if st.session_state.player["社交"] < 15:
                st.session_state.player["學業"] -= 3
                msg_list.append("💀 【邊緣人危機】錯過作業改期限的情報，學業下降。")

            # 結算固定時間事件
            if st.session_state.week in [8, 17]:
                st.session_state.player["學業"] += 5
                msg_list.append("📝 【助教洩題】考前拿到重點筆記，學業大幅提升！")

            if st.session_state.week in [9, 18]:
                score = st.session_state.player["學業"] + random.randint(-10, 10)
                msg_list.append(f"💯 【期中/期末考結束】你的表現評分為：{score}。")

            # 隨機抽取一般事件或選擇事件 (70% 機率觸發)
            if random.random() < 0.70:
                if random.random() < 0.5:
                    # 觸發選擇事件，設定 ID 並阻斷下週常規畫面
                    st.session_state.pending_choice = random.randint(1, 5)
                else:
                    # 觸發一般隨機事件 (10種)
                    rand_ev = random.randint(1, 10)
                    if rand_ev == 1:
                        money = random.choice([2, 6, 10])
                        st.session_state.player["存款"] += money
                        msg_list.append(f"🔔 發票中獎獲得 {money}00 元！(存款+{money})")
                    elif rand_ev == 2:
                        st.session_state.player["健康"] -= 5
                        st.session_state.ap = max(0, st.session_state.ap - 10)
                        msg_list.append("🔔 台南太熱導致中暑！(健康-5, AP-10)")
                    elif rand_ev == 3:
                        st.session_state.player["健康"] += 3
                        st.session_state.player["社交"] += 3
                        msg_list.append("🔔 學長姐請客吃直屬聚！(健康+3, 社交+3)")
                    elif rand_ev == 4:
                        st.session_state.player["存款"] -= 10
                        msg_list.append("🔔 機車違停被拖吊了...(存款-10)")
                    elif rand_ev == 5:
                        st.session_state.player["存款"] -= 15
                        msg_list.append("🔔 停在火車站的腳踏車被偷了！(存款-15)")
                    elif rand_ev == 6:
                        if st.session_state.prof_treat_count < 2:
                            st.session_state.player["健康"] += 5
                            st.session_state.player["社交"] += 5
                            st.session_state.player["學業"] += 2
                            st.session_state.prof_treat_count += 1
                            msg_list.append("🔔 教授請客吃導生聚！(健康+5, 社交+5, 學業+2)")
                        else:
                            st.session_state.player["存款"] += 5
                            msg_list.append("🔔 走在路上撿到 500 塊！(存款+5)")  # 替代方案
                    elif rand_ev == 7:
                        st.session_state.player["學業"] += 5
                        st.session_state.player["健康"] += 3
                        msg_list.append("🔔 通識課遇到神仙組員包辦報告！(學業+5, 健康+3)")
                    elif rand_ev == 8:
                        st.session_state.player["存款"] += 20
                        msg_list.append("🔔 申請的獎學金/補助入帳了！(存款+20)")
                    elif rand_ev == 9:
                        st.session_state.player["學業"] -= 5
                        st.session_state.player["健康"] -= 3
                        msg_list.append("🔔 死線前筆電當機，熬夜重打報告...(學業-5, 健康-3)")
                    elif rand_ev == 10:
                        st.session_state.player["存款"] -= 8
                        st.session_state.player["健康"] -= 5
                        msg_list.append("🔔 在光復校區腳踏車犁田摔壞手機！(存款-8, 健康-5)")

            # 清除翹課計數，推進週次，合併訊息
            st.session_state.skip_count = 0
            st.session_state.week += 1
            st.session_state.event_message = "\n\n".join(msg_list) if msg_list else "本週平安無事地開始了。"
            st.rerun()

# ==========================================
# 4. 結局畫面 (第 18 週之後)
# ==========================================
elif st.session_state.game_started and st.session_state.week > 18:
    st.header("🎓 遊戲結束！成大生活結算")

    f_aca = st.session_state.player["學業"]
    f_hp = st.session_state.player["健康"]
    f_wlt = st.session_state.player["存款"]
    f_soc = st.session_state.player["社交"]

    st.subheader("最終狀態")
    st.write(f"📚 學業：{f_aca} | 💪 健康：{f_hp} | 💰 存款：{f_wlt} | 🤝 社交：{f_soc}")

    st.divider()
    st.subheader("🌟 你的專屬結局")

    if f_aca >= 80 and f_hp < 20:
        st.success("【爆肝學霸】拿到了書卷獎，但每天熬夜喝牛肉湯，身體快扛不住啦！")
    elif f_soc >= 80:
        st.success("【公關達人】走到育樂街都有認識的攤販老闆，台南簡直是你的主場！")
    elif f_wlt >= 80:
        st.success("【學生富豪】打工賺得比正職還多，學分什麼的就當作交朋友吧！")
    elif f_aca < 30:
        st.error("【延畢大師】這學期的學分岌岌可危，準備多留一年吃丹丹漢堡了...")
    else:
        st.info("【平凡大學生】平安順利度過了充實的一學期，穩穩當當也是一種幸福！")

    st.divider()
    if st.button("🔄 重新開始大學生活"):
        st.session_state.clear()
        st.rerun()