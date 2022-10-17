
async def comission(order_sum: [int, float]):
    percent = await check_comission()
    try:
        return order_sum * (1 + percent / 100)
    except Exception as e:
        print(e)


async def check_comission():
    comission_number = 2
    return comission_number
