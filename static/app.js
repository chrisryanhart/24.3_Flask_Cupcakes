
const $body = $('body');
const $h2 = $('<h2>');
const $ul = $('#list');
const $submitForm = $('#submit-form');


async function getCupcakes(){
    let res = await axios.get('http://127.0.0.1:5000/api/cupcakes')
    let data = res.data;

    return res.data;
}

async function populateCupcakes(){
    let data = await getCupcakes();
    let list = data.cupcakes

    for(cupcake in list){
        $li=$(`<li> ${list[cupcake].flavor} </li>`);
        $ul.append($li);
    }
}

populateCupcakes();


$submitForm.on('submit', async function(evt){
    evt.preventDefault();

    let $flavor = $('#flavor').val();
    let $size = $('#size').val();
    let $rating = $('#rating').val();
    let $image = $('#image').val();

    let res = await axios.post('/api/cupcakes',{'flavor':`${$flavor}` , 'size':`${$size}`, 'rating':`${$rating}`, 'image':`${$image}`});
    let cupcake = res.data.cupcake;

    addCupcake(cupcake);

    $submitForm.trigger('reset');
});

function addCupcake(cupcake){
    let flavor = cupcake.flavor;

    $li=$(`<li> ${flavor} </li>`);    
    $ul.append($li);
}





