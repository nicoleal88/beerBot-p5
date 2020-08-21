var timeFormat = 'MM/DD/YYYY HH:mm';

async function getData() {
    const response = await fetch('/tenmin');
    const data = await response.json();
    // console.log(data);
    return data;
}

async function plotIt() {
    const data = await getData();
    let t1 = []
    let t2 = []
    let t3 = []
    let timestamp = [];
    console.log(data);
    for (item of data) {
        t1.push(item.t1);
        t2.push(item.t2);
        t3.push(item.t3);
        timestamp.push(item.timestamp);
    }
    console.log(t1);
    console.log(timestamp);
    var ctx = document.getElementById("myChart").getContext("2d");
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: timestamp,
            datasets: [{
                    label: "Fermentador 1",
                    data: t1,
                    borderColor: 'rgb(255, 99, 132)'
                },
                {
                    label: "Fermentador 2",
                    data: t2,
                    borderColor: 'rgb(255, 255, 132)'
                }
            ]
        },
        options: {
            title: {
                display: true,
                text: 'Últimos 10 minutos'
            },
            responsive: true,
            maintainAspectRatio: false
        }
    });
}

plotIt();