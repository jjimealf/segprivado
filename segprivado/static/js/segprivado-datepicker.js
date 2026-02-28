(function () {
    const WEEKDAYS = ["L", "M", "X", "J", "V", "S", "D"];
    const monthFormatter = new Intl.DateTimeFormat("es-ES", {
        month: "long",
        year: "numeric"
    });

    function parseIsoDate(value) {
        if (!value || !/^\d{4}-\d{2}-\d{2}$/.test(value)) {
            return null;
        }

        const parsed = new Date(value + "T00:00:00");
        return Number.isNaN(parsed.getTime()) ? null : stripTime(parsed);
    }

    function stripTime(date) {
        return new Date(date.getFullYear(), date.getMonth(), date.getDate());
    }

    function toIsoDate(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, "0");
        const day = String(date.getDate()).padStart(2, "0");
        return year + "-" + month + "-" + day;
    }

    function sameDay(a, b) {
        return a && b
            && a.getFullYear() === b.getFullYear()
            && a.getMonth() === b.getMonth()
            && a.getDate() === b.getDate();
    }

    function startOfMonth(date) {
        return new Date(date.getFullYear(), date.getMonth(), 1);
    }

    function buildPicker(input, options) {
        const host = input.closest(".appointment-date-field") || input.parentElement;
        const minDate = parseIsoDate(options.minDate || input.dataset.minDate);
        const today = stripTime(new Date());
        const initialSelected = parseIsoDate(input.value);
        const state = {
            minDate: minDate,
            selectedDate: initialSelected,
            viewDate: startOfMonth(initialSelected || minDate || today)
        };

        host.classList.add("sp-date-picker-host");
        input.readOnly = true;
        input.setAttribute("inputmode", "none");
        input.setAttribute("aria-haspopup", "dialog");

        const picker = document.createElement("div");
        picker.className = "sp-date-picker";
        picker.hidden = true;
        picker.innerHTML = [
            '<div class="sp-date-picker__header">',
            '<button class="sp-date-picker__nav" type="button" data-nav="prev" aria-label="Mes anterior"><</button>',
            '<div class="sp-date-picker__month" data-role="month"></div>',
            '<button class="sp-date-picker__nav" type="button" data-nav="next" aria-label="Mes siguiente">></button>',
            "</div>",
            '<div class="sp-date-picker__weekdays" data-role="weekdays"></div>',
            '<div class="sp-date-picker__days" data-role="days"></div>'
        ].join("");
        host.appendChild(picker);

        const monthLabel = picker.querySelector('[data-role="month"]');
        const weekdaysGrid = picker.querySelector('[data-role="weekdays"]');
        const daysGrid = picker.querySelector('[data-role="days"]');

        WEEKDAYS.forEach(function (weekday) {
            const cell = document.createElement("div");
            cell.className = "sp-date-picker__weekday";
            cell.textContent = weekday;
            weekdaysGrid.appendChild(cell);
        });

        function render() {
            monthLabel.textContent = monthFormatter.format(state.viewDate);
            daysGrid.innerHTML = "";

            const firstDayOfMonth = startOfMonth(state.viewDate);
            const mondayOffset = (firstDayOfMonth.getDay() + 6) % 7;
            const gridStart = new Date(firstDayOfMonth);
            gridStart.setDate(firstDayOfMonth.getDate() - mondayOffset);

            for (let index = 0; index < 42; index += 1) {
                const currentDate = new Date(gridStart);
                currentDate.setDate(gridStart.getDate() + index);

                const dayButton = document.createElement("button");
                dayButton.type = "button";
                dayButton.className = "sp-date-picker__day";
                dayButton.textContent = String(currentDate.getDate());
                dayButton.dataset.value = toIsoDate(currentDate);

                if (currentDate.getMonth() !== state.viewDate.getMonth()) {
                    dayButton.classList.add("sp-date-picker__day--outside");
                }

                if (sameDay(currentDate, today)) {
                    dayButton.classList.add("sp-date-picker__day--today");
                }

                if (sameDay(currentDate, state.selectedDate)) {
                    dayButton.classList.add("sp-date-picker__day--selected");
                }

                if (state.minDate && currentDate < state.minDate) {
                    dayButton.disabled = true;
                    dayButton.classList.add("sp-date-picker__day--disabled");
                }

                daysGrid.appendChild(dayButton);
            }
        }

        function openPicker() {
            state.selectedDate = parseIsoDate(input.value) || state.selectedDate;
            state.viewDate = startOfMonth(state.selectedDate || state.minDate || today);
            picker.hidden = false;
            input.setAttribute("aria-expanded", "true");
            render();
        }

        function closePicker() {
            picker.hidden = true;
            input.setAttribute("aria-expanded", "false");
        }

        function changeMonth(delta) {
            state.viewDate = new Date(state.viewDate.getFullYear(), state.viewDate.getMonth() + delta, 1);
            render();
        }

        function selectDate(value) {
            input.value = value;
            state.selectedDate = parseIsoDate(value);
            input.dispatchEvent(new Event("input", { bubbles: true }));
            input.dispatchEvent(new Event("change", { bubbles: true }));
            closePicker();
        }

        input.addEventListener("focus", openPicker);
        input.addEventListener("click", openPicker);
        input.addEventListener("keydown", function (event) {
            if (event.key === "Escape") {
                closePicker();
                return;
            }

            if (event.key === "Enter" || event.key === " " || event.key === "ArrowDown") {
                event.preventDefault();
                openPicker();
            }
        });

        picker.addEventListener("click", function (event) {
            const navButton = event.target.closest("[data-nav]");
            if (navButton) {
                changeMonth(navButton.dataset.nav === "prev" ? -1 : 1);
                return;
            }

            const dayButton = event.target.closest(".sp-date-picker__day");
            if (!dayButton || dayButton.disabled) {
                return;
            }

            selectDate(dayButton.dataset.value);
        });

        document.addEventListener("pointerdown", function (event) {
            if (!host.contains(event.target)) {
                closePicker();
            }
        });

        document.addEventListener("keydown", function (event) {
            if (event.key === "Escape") {
                closePicker();
            }
        });
    }

    window.SegPrivadoDatePicker = {
        attach: function (target, options) {
            const input = typeof target === "string" ? document.querySelector(target) : target;

            if (!input || input.dataset.spDatePickerAttached === "true") {
                return;
            }

            input.dataset.spDatePickerAttached = "true";
            buildPicker(input, options || {});
        }
    };
}());
