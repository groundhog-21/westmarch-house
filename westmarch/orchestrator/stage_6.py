        # -----------------------------
        # STAGE 6 – Parallel Analysis Round
        # Perkins + Pennington in parallel tracks
        # -----------------------------

        # 23. Jeeves proposes a structured investigation round
        jeeves_parallel_instruction = (
            "Propose a structured 'Parallel Analysis Round' to the household. "
            "Ask Perkins to run a focused metadata scan near the iron door, "
            "and Miss Pennington to prepare an addendum to her Discrepancy Report "
            "for Archive Chamber B. Stay calm and orderly."
        )
        jeeves_parallel_msg = make_message(
            sender="Patron",
            recipient="Jeeves",
            task=TaskType.CONVERSATION,
            content=jeeves_parallel_instruction,
        )
        jeeves_parallel_reply = self.jeeves.run(jeeves_parallel_msg)

        add_ui(
            role="assistant",
            speaker="Jeeves",
            content=f"🎩 Jeeves → 📚 Perkins & ✒️ Pennington:\n{jeeves_parallel_reply}",
        )

        # 24. Perkins calls the Archival Metadata Scrutinizer v3.2 (custom tool)
        tool_output = self._run_archival_metadata_scrutinizer()

        perkins_tool_instruction = (
            "You are standing near the iron door in Archive Chamber B. "
            "You have just received the following output from the Archival Metadata "
            "Scrutinizer v3.2:\n\n"
            f"{tool_output}\n\n"
            "Interpret this data in your analytical, slightly dramatic style. "
            "Comment on ambient dread, tremor frequency, and any implications "
            "for the iron door itself. Keep to 3–4 sentences."
        )
        perkins_tool_msg = make_message(
            sender="Jeeves",
            recipient="Perkins",
            task=TaskType.RESEARCH,
            content=perkins_tool_instruction,
        )
        perkins_tool_reply = self.perkins.run(perkins_tool_msg)

        add_ui(
            role="assistant",
            speaker="Perkins",
            content=f"📚 Perkins (Tool Report):\n{perkins_tool_reply}",
        )

        # 25. Pennington prepares a Discrepancy Report Addendum (parallel track)
        pennington_addendum_instruction = (
            "Draft a brief 'Discrepancy Report – Addendum' for Archive Chamber B. "
            "Note specifically: (1) the iron door's continued undocumented status, "
            "(2) the use of the Archival Metadata Scrutinizer v3.2, "
            "(3) any worrying trends in 'ambient dread' readings. "
            "Keep it tidy and bureaucratically composed."
        )
        pennington_addendum_msg = make_message(
            sender="Jeeves",
            recipient="Miss Pennington",
            task=TaskType.DRAFTING,
            content=pennington_addendum_instruction,
        )
        pennington_addendum_reply = self.pennington.run(pennington_addendum_msg)

        add_ui(
            role="assistant",
            speaker="Miss Pennington",
            content=f"✒️ Pennington (Report Addendum):\n{pennington_addendum_reply}",
        )

        # 26. Atmospheric beat
        add_ui(
            role="assistant",
            speaker="Narrator",
            content=(
                "🏰 *The Scrutinizer’s last clicks fade into stillness. "
                "The iron door remains shut, its surface dull and unmoving, "
                "while the chamber air feels faintly denser than before.*"
            ),
        )


        # -----------------------------
        # STAGE 7 – Long-Running Pause / Resume
        # -----------------------------

        # 27. Sudden mechanical interruption (system voice)
        add_ui(
            role="assistant",
            speaker="Narrator",
            content=(
                "🏰 *A sudden grinding clatter erupts overhead as the Automated "
                "Stack Carousel lurches into motion, sending a tremor through the "
                "shelves and a faint shiver across the iron door’s frame.*"
            ),
        )

        # 28. Scripted Patron: suggest pausing
        add_ui(
            role="user",
            speaker="user",
            content=(
                "👤 Patron: Jeeves, perhaps we should pause the investigation "
                "until that infernal machinery settles."
            ),
        )

        # 29. Jeeves: acknowledge pause and later resume
        jeeves_pause_instruction = (
            "Acknowledge the Patron's request to pause the investigation while the "
            "Automated Stack Carousel is in motion. "
            "Confirm that you will resume once conditions are stable. "
            "Then, in the same reply, mark the moment of 'resuming' the investigation, "
            "as though some time has passed. 2–3 sentences total."
        )
        jeeves_pause_msg = make_message(
            sender="Patron",
            recipient="Jeeves",
            task=TaskType.CONVERSATION,
            content=jeeves_pause_instruction,
        )
        jeeves_pause_reply = self.jeeves.run(jeeves_pause_msg)

        add_ui(
            role="assistant",
            speaker="Jeeves",
            content=f"🎩 Jeeves: {jeeves_pause_reply}",
        )

        # 30. Narrator marks the passage of time (long-running operation flavor)
        add_ui(
            role="assistant",
            speaker="Narrator",
            content=(
                "🏰 *The machinery above grinds on for a time, then stills. "
                "Dust settles back onto ledgers and ledges alike. "
                "The iron door waits, unchanged in position, patient and mute.*"
            ),
        )

        # 31. Perkins proposes repeating the scan (loop agent behavior)
        perkins_loop_instruction = (
            "Now that the disturbance has passed, propose running another metadata "
            "scan to compare readings before and after the mechanical interruption. "
            "Sound methodical and faintly excited."
        )
        perkins_loop_msg = make_message(
            sender="Narrator",
            recipient="Perkins",
            task=TaskType.RESEARCH,
            content=perkins_loop_instruction,
        )
        perkins_loop_reply = self.perkins.run(perkins_loop_msg)

        add_ui(
            role="assistant",
            speaker="Perkins",
            content=f"📚 Perkins (Loop Proposal):\n{perkins_loop_reply}",
        )

        # -----------------------------
        # STAGE 8 – Loop Scan + Resolution
        # Perkins runs Metadata Scan #2 and compares results
        # Pennington logs final anomalies
        # Jeeves coordinates the resolution
        # Hawthorne delivers closing wit
        # -----------------------------

        # 32. Activate Scrutinizer again (Loop Round 2)
        second_tool_output = self._run_archival_metadata_scrutinizer()

        perkins_loopscan_instruction = (
            "You have now performed a SECOND metadata scan immediately after the "
            "mechanical disturbance has settled. Here are the new Scrutinizer readings:\n\n"
            f"{second_tool_output}\n\n"
            "Compare these with the earlier readings. Identify any changes in "
            "'ambient dread', tremor frequency, or foreign particle distribution. "
            "Offer a 3–4 sentence interpretation in your analytical, faintly theatrical style."
        )
        perkins_loopscan_msg = make_message(
            sender="Jeeves",
            recipient="Perkins",
            task=TaskType.RESEARCH,
            content=perkins_loopscan_instruction,
        )
        perkins_loopscan_reply = self.perkins.run(perkins_loopscan_msg)

        add_ui(
            role="assistant",
            speaker="Perkins",
            content=f"📚 Perkins (Comparative Metadata Report):\n{perkins_loopscan_reply}",
        )

        # 33. Pennington logs the final anomaly report
        pennington_final_instruction = (
            "Draft the concluding section of an 'Anomalous Door – Summary Assessment'. "
            "Include: (1) two metadata scans performed, (2) consistency in 'ambient dread' levels, "
            "(3) confirmation that the iron door remains undocumented, (4) any bureaucratic "
            "recommendations for future monitoring. Keep it concise, meticulous, and calm."
        )
        pennington_final_msg = make_message(
            sender="Perkins",
            recipient="Miss Pennington",
            task=TaskType.DRAFTING,
            content=pennington_final_instruction,
        )
        pennington_final_reply = self.pennington.run(pennington_final_msg)

        add_ui(
            role="assistant",
            speaker="Miss Pennington",
            content=f"✒️ Pennington (Summary Assessment):\n{pennington_final_reply}",
        )

        # 34. Jeeves provides a composed resolution summary to the Patron
        jeeves_resolution_instruction = (
            "Summarize the investigation results with impeccable composure. "
            "Note that two metadata scans produced stable readings, the iron door remains "
            "closed, no hazardous fluctuations are presently indicated, and the chamber's "
            "conditions have normalized. Offer to continue monitoring if the Patron desires. "
            "Keep to 2–3 sentences."
        )
        jeeves_resolution_msg = make_message(
            sender="Miss Pennington",
            recipient="Jeeves",
            task=TaskType.CONVERSATION,
            content=jeeves_resolution_instruction,
        )
        jeeves_resolution_reply = self.jeeves.run(jeeves_resolution_msg)

        add_ui(
            role="assistant",
            speaker="Jeeves",
            content=f"🎩 Jeeves → Patron:\n{jeeves_resolution_reply}",
        )

        # 35. Lady Hawthorne’s closing commentary (lightly mocking)
        hawthorne_exit_instruction = (
            "Deliver a refined, slightly mocking commentary on the entire investigation. "
            "Tease the household for conducting such earnest scrutiny of a stationary iron door. "
            "Maintain your theatrical disdain but avoid cruelty. "
            "2–3 sentences."
        )
        hawthorne_exit_msg = make_message(
            sender="Jeeves",
            recipient="Lady Hawthorne",
            task=TaskType.CONVERSATION,
            content=hawthorne_exit_instruction,
        )
        hawthorne_exit_reply = self.hawthorne.run(hawthorne_exit_msg)

        add_ui(
            role="assistant",
            speaker="Lady Hawthorne",
            content=f"🕯️ Lady Hawthorne (Exit Commentary):\n{hawthorne_exit_reply}",
        )

        # 36. Final atmospheric outro (Narrator)
        add_ui(
            role="assistant",
            speaker="Narrator",
            content=(
                "🏰 *The quiet settles once more. The iron door stands perfectly still, "
                "its surface unreflective, its outline unchanged. Nothing moves but the "
                "dust drifting lazily in the lamplight.*"
            ),
        )