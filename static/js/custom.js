function SendArticleCommend(ArticleId) {
    // console.log('hello world');

    var commend = $('#commendText').val();
    var parentId = $("#parent_id").val();

    $.get('/article/add-article-commend', {
        article_comment: commend,
        article_id: ArticleId,
        parent_id: parentId
    }).then(res => {
        console.log(res);
        location.reload();
        $('#commendText').val('');
        $('#parent_id').val('');
        document.getElementById('commendText').scrollIntoView({behavior: 'smooth'});
    })
}

function fillParentId(parentId) {
    $("#parent_id").val(parentId);
    document.getElementById('commentForm').scrollIntoView({behavior: 'smooth'});
}

function filterProducts() {
    const filterPrice = $('#sl2').val();
    const start_price = filterPrice.split(',')[0];
    const end_price = filterPrice.split(',')[1];
    $('#start_price').val(start_price);
    $('#end_price').val(end_price);
    $('#filter_form').submit();
}


function fillPage(page) {
    $('#page').val(page);
    $('#filter_form').submit();
}


function ShowLargeImage(imageAddress) {
    $('#main_image').attr('src', imageAddress);
}


function AddProductToOrder(productId) {
    const productCount = $('#product-count').val();
    $.get('/order/add-to-order?product_id=' + productId + '&count=' + productCount).then(res => {
            Swal.fire({
                title: 'اعلان',
                text: res.text,
                icon: res.icon,
                showCancelButton: false,
                confirmButtonColor: '#3085d6',
                confirmButtonText: res.confirmButtonText
            }).then(result => {
                if (result.isConfirmed && res.status === 'not_auth') {
                    window.location.href = "/login";
                }
            });
        }
    )
}

function RemoveOrderDetail(detailId) {
    $.get('/user/remove-order-detail?detail_id=' + detailId).then(res => {
        if (res.status === 'success'){
            $('#order-detail-content').html(res.body);
        }
    });
}

function ChangeOrderDetailCount(detailId, state) {
    $.get('/user/change-order-detail?detail_id=' + detailId+ '&state='+ state).then(res => {
        if (res.status === 'success'){
            $('#order-detail-content').html(res.body);
        }
    });
}
