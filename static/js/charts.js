const categoryCtx = document.getElementById('categoryChart');

new Chart(categoryCtx, {
type: 'pie',

data: {
labels: ['Complaint','Query','Feedback'],

datasets: [{
data: [
categoryData.complaints,
categoryData.queries,
categoryData.feedback
],

backgroundColor:[
'#ef4444',
'#3b82f6',
'#10b981'
]

}]
}

});


const sentimentCtx = document.getElementById('sentimentChart');

new Chart(sentimentCtx, {

type:'bar',

data:{
labels:['Positive','Neutral','Negative'],

datasets:[{

label:'Sentiment',

data:[
sentimentData.positive,
sentimentData.neutral,
sentimentData.negative
],

backgroundColor:[
'#22c55e',
'#f59e0b',
'#ef4444'
]

}]

}

});