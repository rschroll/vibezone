window.onload = function() {
    // Set from timezone to user's current timezone
    const userTZ = Intl.DateTimeFormat().resolvedOptions().timeZone;
    document.getElementById('from_timezone').value = userTZ;

    // Set start and end datetime to next top of the hour and one hour later
    const now = new Date();
    const nextHour = new Date(now);
    nextHour.setHours(now.getHours() + 1, 0, 0, 0);
    const hourAfter = new Date(nextHour);
    hourAfter.setHours(nextHour.getHours() + 1);

    // Format for datetime-local (YYYY-MM-DDTHH:MM)
    const formatDateTime = (date) => {
        return date.toISOString().slice(0, 16);
    };

    document.getElementById('start_datetime').value = formatDateTime(nextHour);
    document.getElementById('end_datetime').value = formatDateTime(hourAfter);

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
