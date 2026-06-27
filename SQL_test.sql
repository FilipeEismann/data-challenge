SELECT dp.PRODUCT_COD,
	   dp.PRODUCT_NAME,
	   dp.PRODUCT_VAL 
FROM data_product dp
ORDER BY dp.PRODUCT_VAL DESC
LIMIT 10
/* 
Whisky Escoces THE MACALLAN Ruby Garrafa 700ml com Caixa
Whisky Escoces JOHNNIE WALKER Blue Label Garrafa 750ml
Cafeteira Expresso 3 CORACOES Tres Modo Vermelho
Vinho Portugues Tinto Vintage QUINTA DO CRASTO Garrafa 750ml
Escova Dental Eletrica ORAL B D34 Professional Care 5000 110v
Champagne Rose VEUVE CLICQUOT PONSARDIM Garrafa 750ml
Champagne Frances Brut Imperial MOET Rose Garrafa 750ml
Conjunto de Panelas Allegra em Inox TRAMONTINA 5 Pecas Gratis Utensilios 5 Pecas
Whisky Escoces CHIVAS REGAL 18 Anos Garrafa 750ml
Champagne Frances Brut Imperial MOET & CHANDON Garrafa 750ml 
*/
;

SELECT DISTINCT dp.DEP_NAME,
	   			dp.SECTION_NAME
FROM data_product dp 
WHERE dp.DEP_NAME in ('BEBIDAS', 'PADARIA')
ORDER BY 1 ASC
/* Bebidas: Bebidas, Cervejas, Refrescos e Vinhos */
/* Padaria: Doces e Sobremesas, Gestante, Padaria, Queijos e Frios */
;

SELECT dsc.BUSINESS_CODE,
	   dsc.BUSINESS_NAME,
	   sum(dss.SALES_VALUE) TOTAL_VALUE,
	   sum(dss.SALES_QTY) TOTAL_QTY
FROM data_store_sales dss
INNER JOIN data_store_cad dsc
ON dsc.STORE_CODE = dss.STORE_CODE
WHERE YEAR(dss.DATE) = 2019 
AND QUARTER(dss.DATE) = 1
GROUP BY 1,2
ORDER BY TOTAL_VALUE DESC
/*
Farma		$ 81.776.691,73
Varejo		$ 81.032.347,65
Atacado		$ 80.384.884,60
Proximidade	$ 80.171.122,80
Posto		$ 32.072.326,40
*/
;
