window.onload = function() {
    // Set from timezone to user's current timezone if not already set
    const fromInput = document.getElementById('from_timezone');
    if (fromInput.value === '') {
        const userTZ = Intl.DateTimeFormat().resolvedOptions().timeZone;
        fromInput.value = userTZ;
    }

    // Set start and end datetime to next top of the hour and one hour later if not already set
    const startInput = document.getElementById('start_datetime');
    const endInput = document.getElementById('end_datetime');
    if (startInput.value === '' && endInput.value === '') {
        const now = new Date();
        const nextHour = new Date(now);
        nextHour.setHours(now.getHours() + 1, 0, 0, 0);
        const hourAfter = new Date(nextHour);
        hourAfter.setHours(nextHour.getHours() + 1);

        // Format for datetime-local in local time (YYYY-MM-DDTHH:MM)
        const formatLocalDateTime = (date) => {
            const year = date.getFullYear();
            const month = (date.getMonth() + 1).toString().padStart(2, '0');
            const day = date.getDate().toString().padStart(2, '0');
            const hours = date.getHours().toString().padStart(2, '0');
            const minutes = date.getMinutes().toString().padStart(2, '0');
            return `${year}-${month}-${day}T${hours}:${minutes}`;
        };

        startInput.value = formatLocalDateTime(nextHour);
        endInput.value = formatLocalDateTime(hourAfter);
    }

    // Handle adding timezone inputs
    const container = document.getElementById('to_timezones_container');
    const addButton = document.getElementById('add_tz');

    addButton.addEventListener('click', function() {
        const inputGroups = container.querySelectorAll('.tz-input-group');
        if (inputGroups.length >= 10) {
            alert('Maximum 10 timezones allowed');
            return;
        }
        const firstGroup = inputGroups[0];
        const newGroup = firstGroup.cloneNode(true);
        newGroup.querySelector('input').value = '';
        container.insertBefore(newGroup, addButton);
        updateRemoveButtons();
    });

    // Handle removing timezone inputs
    container.addEventListener('click', function(e) {
        if (e.target.classList.contains('remove-tz')) {
            const inputGroups = container.querySelectorAll('.tz-input-group');
            if (inputGroups.length > 1) {
                e.target.closest('.tz-input-group').remove();
                updateRemoveButtons();
            }
        }
    });

    function updateRemoveButtons() {
        const inputGroups = container.querySelectorAll('.tz-input-group');
        inputGroups.forEach((group, index) => {
            const removeBtn = group.querySelector('.remove-tz');
            removeBtn.style.display = inputGroups.length > 1 ? '' : 'none';
        });
    }

    // Initial update
    updateRemoveButtons();
};
