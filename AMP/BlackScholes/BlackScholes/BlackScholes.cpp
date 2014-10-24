#include "BlackScholes.h"
#include <math.h>
#include <amp_math.h>
#include <iostream>
#include <assert.h>

blackscholes::blackscholes(float _volatility, float _riskfreerate, int _size)
{
	data_size = _size;
	riskfreerate = _riskfreerate;
	volatility = _volatility;

	stock_price.resize(data_size);
	option_strike.resize(data_size);
	option_years.resize(data_size);
	call_result_amp.resize(data_size);
	put_result_amp.resize(data_size);

	srand(2014);

	for (int i = 0; i < data_size; i++)
	{
		stock_price[i] = 100.0f * (((float)rand()) / RAND_MAX);
	}

}