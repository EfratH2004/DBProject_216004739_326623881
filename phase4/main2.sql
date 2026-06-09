CREATE OR REPLACE FUNCTION get_low_stock_products(p_limit INT)
RETURNS REFCURSOR
AS $$
DECLARE
    ref REFCURSOR;
BEGIN
    OPEN ref FOR
        SELECT
            pid,
            pname,
            price,
            stock_qty,
            manufactured_in,
            s_id
        FROM products
        WHERE stock_qty IS NOT NULL
          AND stock_qty <= p_limit
        ORDER BY stock_qty ASC, pname ASC;

    RETURN ref;

EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error in get_low_stock_products: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE increase_low_stock_prices_from_cursor(
    p_products_cursor REFCURSOR,
    p_percent NUMERIC DEFAULT 5
)
AS $$
DECLARE
    rec RECORD;
    v_new_price NUMERIC;
    v_counter INT := 0;
BEGIN
    IF p_percent <= 0 THEN
        RAISE EXCEPTION 'Percent must be positive';
    END IF;

    LOOP
        FETCH p_products_cursor INTO rec;
        EXIT WHEN NOT FOUND;

        v_new_price := rec.price + (rec.price * p_percent / 100);

        UPDATE products
        SET price = ROUND(v_new_price)::INT
        WHERE pid = rec.pid;

        v_counter := v_counter + 1;

        RAISE NOTICE 'Product % price updated from % to % using % percent',
            rec.pname,
            rec.price,
            ROUND(v_new_price)::INT,
            p_percent;
    END LOOP;

    RAISE NOTICE 'Total products updated: %', v_counter;

EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error in increase_low_stock_prices_from_cursor: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;


-- טריגר 2:
CREATE OR REPLACE FUNCTION validate_price_increase()
RETURNS TRIGGER
AS $$
BEGIN

    IF NEW.price > OLD.price * 1.20 THEN
        RAISE EXCEPTION
            'Price increase too high for product %. Old price: %, New price: %',
            NEW.pid,
            OLD.price,
            NEW.price;
    END IF;

    RETURN NEW;

END;
$$ LANGUAGE plpgsql;


DROP TRIGGER IF EXISTS trg_validate_price_increase ON products;

CREATE TRIGGER trg_validate_price_increase
BEFORE UPDATE OF price ON products
FOR EACH ROW
EXECUTE FUNCTION validate_price_increase();



BEGIN;

DO $$
DECLARE
    c REFCURSOR;
    v_stock_limit INT := 10;
    v_price_update_percent NUMERIC := 5;
BEGIN
    RAISE NOTICE 'Main stock process started';

    c := get_low_stock_products(v_stock_limit);

    CALL increase_low_stock_prices_from_cursor(c, v_price_update_percent);

    CLOSE c;

    RAISE NOTICE 'Main stock process finished';
END;
$$;

COMMIT;