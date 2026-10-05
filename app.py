import streamlit as st
import random


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Chor Police",
    page_icon="👑",
    layout="centered"
)


# ---------------- SESSION STATE ----------------

if "players" not in st.session_state:
    st.session_state.players = []

if "game_players" not in st.session_state:
    st.session_state.game_players = []

if "winner" not in st.session_state:
    st.session_state.winner = None

if "game_started" not in st.session_state:
    st.session_state.game_started = False

if "game_finished" not in st.session_state:
    st.session_state.game_finished = False

if "sipahi_name" not in st.session_state:
    st.session_state.sipahi_name = None

# Number of rounds
if "max_rounds" not in st.session_state:
    st.session_state.max_rounds = 1

# Current round
if "round_number" not in st.session_state:
    st.session_state.round_number = 1

# Total scores
if "total_scores" not in st.session_state:
    st.session_state.total_scores = {}

# Result of previous round
if "round_message" not in st.session_state:
    st.session_state.round_message = None

if "round_correct" not in st.session_state:
    st.session_state.round_correct = None

if "last_chor_name" not in st.session_state:
    st.session_state.last_chor_name = None


# ---------------- ROLES ----------------

roles = ["Raja", "Rani", "Sipahi", "Chor"]


# ---------------- SCORES ----------------

role_scores = {
    "Raja": 10000,
    "Rani": 5000,
    "Sipahi": 100,
    "Chor": 0
}


# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

.title {
    text-align: center;
    font-size: 45px;
    font-weight: bold;
    color: #facc15;
}

.subtitle {
    text-align: center;
    color: #cbd5e1;
    font-size: 20px;
    margin-bottom: 30px;
}

.player-card {
    background-color: #1e293b;
    padding: 18px;
    border-radius: 15px;
    margin: 10px 0;
    border: 1px solid #334155;
}

.sipahi-card {
    background-color: #172554;
    padding: 20px;
    border-radius: 18px;
    text-align: center;
    border: 2px solid #60a5fa;
    margin: 20px 0;
}

.winner {
    background-color: #422006;
    padding: 25px;
    border-radius: 20px;
    text-align: center;
    border: 2px solid #facc15;
}

</style>
""", unsafe_allow_html=True)


# ==================================================
# HOME / JOIN PAGE
# ==================================================

if (
    not st.session_state.game_started
    and not st.session_state.game_finished
):

    st.markdown(
        '<div class="title">👑 Raja Mantri Chor Sipahi</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">🎮 Chor Police Game</div>',
        unsafe_allow_html=True
    )

    st.write(
        f"### 👥 Players: "
        f"{len(st.session_state.players)}/4"
    )


    # ---------------- PLAYER NAME ----------------

    name = st.text_input(
        "Enter Player Name",
        placeholder="Example: Amish"
    )


    # ---------------- JOIN BUTTON ----------------

    if st.button(
        "➕ Join Game",
        use_container_width=True
    ):

        player_name = name.strip()

        if not player_name:

            st.warning("Please enter your name.")

        elif len(st.session_state.players) >= 4:

            st.error("Game is already full!")

        elif player_name in st.session_state.players:

            st.warning("This player has already joined.")

        else:

            st.session_state.players.append(
                player_name
            )

            st.success(
                f"{player_name} joined the game!"
            )

            st.rerun()


    # ---------------- DISPLAY PLAYERS ----------------

    if st.session_state.players:

        st.subheader("👥 Joined Players")

        for i, player in enumerate(
            st.session_state.players,
            start=1
        ):

            st.markdown(
                f"""
                <div class="player-card">
                    <strong>Player {i}</strong><br>
                    👤 {player}
                </div>
                """,
                unsafe_allow_html=True
            )


    # ---------------- START GAME ----------------

    if len(st.session_state.players) == 4:

        st.success(
            "🎉 4 players joined! Ready to start."
        )

        # ---------------- SELECT NUMBER OF ROUNDS ----------------

        selected_rounds = st.selectbox(
            "🔄 How many rounds would you like to play?",
            list(range(1, 21)),
            index=4
        )


        if st.button(
            "🎮 Start Game",
            use_container_width=True
        ):

            # Save selected rounds
            st.session_state.max_rounds = selected_rounds

            # Start from round 1
            st.session_state.round_number = 1

            # Reset winner
            st.session_state.winner = None

            # Reset messages
            st.session_state.round_message = None
            st.session_state.round_correct = None
            st.session_state.last_chor_name = None

            # Reset total scores
            st.session_state.total_scores = {}

            for player in st.session_state.players:

                st.session_state.total_scores[player] = 0


            # ---------------- ASSIGN FIRST ROUND ROLES ----------------

            shuffled_roles = roles.copy()

            random.shuffle(shuffled_roles)

            st.session_state.game_players = []


            for i in range(4):

                st.session_state.game_players.append(
                    {
                        "name": st.session_state.players[i],
                        "role": shuffled_roles[i],
                        "score": 0
                    }
                )


            # ---------------- FIND SIPAHI ----------------

            st.session_state.sipahi_name = None

            for player in st.session_state.game_players:

                if player["role"] == "Sipahi":

                    st.session_state.sipahi_name = (
                        player["name"]
                    )

                    break


            # Start game
            st.session_state.game_started = True

            st.rerun()


# ==================================================
# GAME PAGE
# ==================================================

elif (
    st.session_state.game_started
    and not st.session_state.game_finished
):

    # ==================================================
    # MAIN GAME + SCOREBOARD
    # ==================================================

    game_column, score_column = st.columns(
        [2, 1],
        gap="large"
    )


    # ==================================================
    # GAME COLUMN
    # ==================================================

    with game_column:

        st.markdown(
            '<div class="title">🎮 Game Started</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="subtitle">Find the Chor!</div>',
            unsafe_allow_html=True
        )


        # ---------------- ROUND ----------------

        st.info(
            f"🔄 Round "
            f"{st.session_state.round_number}"
            f" / "
            f"{st.session_state.max_rounds}"
        )


        # ---------------- PREVIOUS ROUND RESULT ----------------

        if st.session_state.round_message:

            if st.session_state.round_correct:

                st.success(
                    f"✅ {st.session_state.round_message}"
                )

            else:

                st.error(
                    f"❌ {st.session_state.round_message}"
                )


        # ---------------- DISPLAY SIPAHI ----------------

        st.markdown(
        f"""
        <div class="sipahi-card">
        <h2>👮 Sipahi</h2>
        <h1>{st.session_state.sipahi_name}</h1>
        <p>This player is the Sipahi.</p>
        </div>
        """,
        unsafe_allow_html=True
        )


        # ---------------- DISPLAY PLAYERS ----------------

        st.subheader("👥 Players")

        for player in st.session_state.game_players:

            st.markdown(
                f"""<div class="player-card">
            👤 <strong>{player["name"]}</strong>
            </div>""",
                unsafe_allow_html=True
            )


        # ---------------- FIND SIPAHI AND CHOR ----------------

        sipahi = None
        chor = None

        for player in st.session_state.game_players:

            if player["role"] == "Sipahi":

                sipahi = player

            elif player["role"] == "Chor":

                chor = player


        # ---------------- SAFETY CHECK ----------------

        if sipahi is None or chor is None:

            st.error(
                "Something went wrong while assigning the roles."
            )

            st.stop()


        st.divider()


        # ---------------- SIPAHI TURN ----------------

        st.subheader("👮 Sipahi's Turn")

        st.write(
            f"**{sipahi['name']}**, choose who you think is the Chor."
        )


        # ---------------- POSSIBLE PLAYERS ----------------

        possible_players = [
            player["name"]
            for player in st.session_state.game_players
            if player["role"] != "Sipahi"
        ]


        # ---------------- SELECT PLAYER ----------------

        guessed_player = st.selectbox(
            "🕵️ Who do you think is the Chor?",
            possible_players
        )


        # ---------------- GUESS BUTTON ----------------

        if st.button(
            "🔍 Guess Chor",
            use_container_width=True
        ):

            # ==================================================
            # CHECK GUESS
            # ==================================================

            if guessed_player == chor["name"]:

                # Correct
                st.session_state.round_message = (
                    f"Correct Guess! "
                    f"{guessed_player} is the Chor."
                )

                st.session_state.round_correct = True

            else:

                # Incorrect
                st.session_state.round_message = (
                    f"Incorrect Guess! "
                    f"The Chor was {chor['name']}."
                )

                st.session_state.round_correct = False


            # Save Chor name
            st.session_state.last_chor_name = chor["name"]


            # ==================================================
            # ADD SCORE FOR CURRENT ROUND
            # ==================================================

            for player in st.session_state.game_players:

                player_name = player["name"]

                player_role = player["role"]

                round_score = role_scores[player_role]

                st.session_state.total_scores[
                    player_name
                ] += round_score


            # ==================================================
            # CHECK LAST ROUND
            # ==================================================

            if (
                st.session_state.round_number
                >= st.session_state.max_rounds
            ):

                # Find highest score
                highest_score = max(
                    st.session_state.total_scores.values()
                )


                # Find winner
                winners = [
                    name
                    for name, score
                    in st.session_state.total_scores.items()
                    if score == highest_score
                ]


                if len(winners) == 1:

                    st.session_state.winner = winners[0]

                else:

                    st.session_state.winner = (
                        " & ".join(winners)
                    )


                # Finish game
                st.session_state.game_started = False

                st.session_state.game_finished = True

                st.rerun()


            # ==================================================
            # NEXT ROUND
            # ==================================================

            else:

                # Increase round
                st.session_state.round_number += 1


                # Shuffle roles
                shuffled_roles = roles.copy()

                random.shuffle(shuffled_roles)


                # Clear current round
                st.session_state.game_players = []


                # Assign new roles
                for i in range(4):

                    st.session_state.game_players.append(
                        {
                            "name": st.session_state.players[i],
                            "role": shuffled_roles[i],
                            "score": 0
                        }
                    )


                # Find new Sipahi
                st.session_state.sipahi_name = None

                for player in st.session_state.game_players:

                    if player["role"] == "Sipahi":

                        st.session_state.sipahi_name = (
                            player["name"]
                        )

                        break


                st.rerun()


    # ==================================================
    # SCOREBOARD COLUMN
    # ==================================================

    with score_column:

        st.subheader("📊 Scoreboard")

        st.write(
            f"Round: "
            f"{st.session_state.round_number}"
            f" / "
            f"{st.session_state.max_rounds}"
        )


        # Create scoreboard data
        scoreboard_data = []

        for player_name, score in (
            st.session_state.total_scores.items()
        ):

            scoreboard_data.append(
                {
                    "Player": player_name,
                    "Score": score
                }
            )


        # Sort highest score first
        scoreboard_data.sort(
            key=lambda x: x["Score"],
            reverse=True
        )


        # Display table
        st.dataframe(
            scoreboard_data,
            use_container_width=True,
            hide_index=True
        )


        st.divider()


        st.write("### 🎯 Points")

        st.write("👑 Raja = **10,000**")

        st.write("👸 Rani = **5,000**")

        st.write("👮 Sipahi = **100**")

        st.write("🕵️ Chor = **0**")


# ==================================================
# RESULT PAGE
# ==================================================

elif st.session_state.game_finished:

    st.markdown(
        '<div class="title">🏆 Game Result</div>',
        unsafe_allow_html=True
    )


    # ---------------- WINNER ----------------

    winner = st.session_state.winner

    st.markdown(
        f"""<div class="winner">
    <h2>🎉 Winner</h2>
    <h1>{winner}</h1>
    </div>""",
        unsafe_allow_html=True
    )


    st.divider()


    # ---------------- FINAL SCORE ----------------

    st.subheader("🏆 Final Scores")


    final_scores = []

    for player_name, score in (
        st.session_state.total_scores.items()
    ):

        final_scores.append(
            {
                "Player": player_name,
                "Final Score": score
            }
        )


    final_scores.sort(
        key=lambda x: x["Final Score"],
        reverse=True
    )


    # Final score table
    st.dataframe(
        final_scores,
        use_container_width=True,
        hide_index=True
    )


    st.divider()


    # ---------------- LAST ROUND RESULT ----------------

    st.subheader("🎯 Last Round Result")

    if st.session_state.round_correct:

        st.success(
            f"✅ {st.session_state.round_message}"
        )

    else:

        st.error(
            f"❌ {st.session_state.round_message}"
        )


    st.divider()


    # ---------------- REVEAL LAST ROUND ROLES ----------------

    st.subheader("🎭 Last Round Roles")

    for player in st.session_state.game_players:

        st.markdown(
            f"""<div class="player-card">
        👤 <strong>{player["name"]}</strong>
        <br>
        🎭 Role:
        <strong>{player["role"]}</strong>
        </div>""",
            unsafe_allow_html=True
        )


    st.divider()


    # ---------------- PLAY AGAIN ----------------

    if st.button(
        "🔄 Play Again",
        use_container_width=True
    ):

        st.session_state.players = []

        st.session_state.game_players = []

        st.session_state.winner = None

        st.session_state.sipahi_name = None

        st.session_state.game_started = False

        st.session_state.game_finished = False

        st.session_state.max_rounds = 1

        st.session_state.round_number = 1

        st.session_state.total_scores = {}

        st.session_state.round_message = None

        st.session_state.round_correct = None

        st.session_state.last_chor_name = None

        st.rerun()