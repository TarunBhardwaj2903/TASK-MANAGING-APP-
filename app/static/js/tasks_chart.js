document.addEventListener('DOMContentLoaded', function () {
    const ctx = document.getElementById('taskChart');

    if (!ctx) return; // Exit if canvas is not found

    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Pending', 'Working', 'Done'],
            datasets: [{
                data: [window.pendingCount, window.workingCount, window.doneCount],
                backgroundColor: ['#f39c12', '#3498db', '#2ecc71'],
                borderColor: ['#ffffff', '#ffffff', '#ffffff'],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#333',
                        font: {
                            size: 14
                        }
                    }
                },
                title: {
                    display: true,
                    text: 'Task Status Overview',
                    font: {
                        size: 16
                    }
                }
            }
        }
    });
});