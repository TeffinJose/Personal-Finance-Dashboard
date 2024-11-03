async function loadChartData(url) {
    const response = await fetch(url);
    const data = await response.json();
    const labels = Object.keys(data);
    const values = Object.values(data);

    new Chart(document.getElementById("expenseChart"), {
        type: "pie",
        data: {
            labels: labels,
            datasets: [{
                label: "Expenses",
                data: values,
                backgroundColor: [
                    "rgba(75, 192, 192, 0.2)",
                    "rgba(255, 99, 132, 0.2)",
                    "rgba(255, 206, 86, 0.2)",
                    "rgba(54, 162, 235, 0.2)"
                ],
                borderColor: [
                    "rgba(75, 192, 192, 1)",
                    "rgba(255, 99, 132, 1)",
                    "rgba(255, 206, 86, 1)",
                    "rgba(54, 162, 235, 1)"
                ],
                borderWidth: 1
            }]
        },
    });
}
