const { Telegraf } = require('telegraf');
const { createClient } = require('@supabase/supabase-js');

const BOT_TOKEN = '8877634770:bot_token'; 
const OWNER_ID = 'your_chat_id'; 
const SUPABASE_URL = 'https://blablabla.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...';

const bot = new Telegraf(BOT_TOKEN);
const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

bot.use((ctx, next) => {
    if (String(ctx.chat.id) !== String(OWNER_ID)) {
        return ctx.reply("🚫 Akses ditolak. Lo bukan owner!");
    }
    return next();
});

function formatUserList(users, page, totalPages, total) {
    let text = `*📋 Daftar User (Halaman ${page+1}/${totalPages})* - Total: ${total}\n\n`;
    users.forEach((user, index) => {
        const created = user.created_at ? new Date(user.created_at).toLocaleString() : 'N/A';
        const expires = user.expires_at ? new Date(user.expires_at).toLocaleString() : 'Unlimited';
        text += `*${index+1 + page*5}.* ID: \`${user.unique_id}\`\n`;
        text += `   Password: \`${user.password || 'Belum diset'}\`\n`;
        text += `   Expired: ${expires}\n`;
        text += `   Dibuat: ${created}\n\n`;
    });
    return text;
}

function getPaginationKeyboard(page, totalPages) {
    const buttons = [];
    if (page > 0) {
        buttons.push({ text: '⬅️ Sebelumnya', callback_data: `page_${page-1}` });
    }
    if (page < totalPages - 1) {
        buttons.push({ text: 'Berikutnya ➡️', callback_data: `page_${page+1}` });
    }
    if (buttons.length === 0) {
        return { inline_keyboard: [] };
    }
    return { inline_keyboard: [buttons] };
}

bot.command('listuser', async (ctx) => {
    const page = 0;
    const limit = 5;
    const offset = page * limit;
    try {
        const { data, error, count } = await supabase
            .from('users')
            .select('*', { count: 'exact' })
            .order('created_at', { ascending: false })
            .range(offset, offset + limit - 1);
        if (error) throw error;
        if (!data || data.length === 0) {
            return ctx.reply('Tidak ada user terdaftar.');
        }
        const total = count;
        const totalPages = Math.ceil(total / limit);
        const message = formatUserList(data, page, totalPages, total);
        const keyboard = getPaginationKeyboard(page, totalPages);
        await ctx.reply(message, {
            parse_mode: 'Markdown',
            reply_markup: keyboard
        });
    } catch (err) {
        ctx.reply(`❌ Error: ${err.message}`);
    }
});

bot.action(/page_(\d+)/, async (ctx) => {
    const page = parseInt(ctx.match[1]);
    const limit = 5;
    const offset = page * limit;
    try {
        const { data, error, count } = await supabase
            .from('users')
            .select('*', { count: 'exact' })
            .order('created_at', { ascending: false })
            .range(offset, offset + limit - 1);
        if (error) throw error;
        if (!data || data.length === 0) {
            await ctx.answerCbQuery('Tidak ada data di halaman ini.');
            return;
        }
        const total = count;
        const totalPages = Math.ceil(total / limit);
        const message = formatUserList(data, page, totalPages, total);
        const keyboard = getPaginationKeyboard(page, totalPages);
        await ctx.editMessageText(message, {
            parse_mode: 'Markdown',
            reply_markup: keyboard
        });
        await ctx.answerCbQuery();
    } catch (err) {
        await ctx.answerCbQuery(`Error: ${err.message}`);
    }
});

bot.command('setpassword', async (ctx) => {
    const args = ctx.message.text.split(' ');
    if (args.length < 3) {
        return ctx.reply('❌ Format salah. Gunakan: `/setpassword <unique_id> <password_baru>`', { parse_mode: 'Markdown' });
    }

    const uniqueId = args[1].trim();
    const newPassword = args.slice(2).join(' ').trim();

    try {
        const { data: checkUser, error: checkError } = await supabase
            .from('users')
            .select('id')
            .eq('unique_id', uniqueId);

        if (checkError || !checkUser || checkUser.length === 0) {
            return ctx.reply(`❌ Gagal: ID \`${uniqueId}\` gak ditemukan di database!`, { parse_mode: 'Markdown' });
        }

        const { error } = await supabase
            .from('users')
            .update({ password: newPassword })
            .eq('unique_id', uniqueId);

        if (error) {
            ctx.reply(`❌ Gagal update password: ${error.message}`);
        } else {
            ctx.reply(`✅ Password untuk ID \`${uniqueId}\` berhasil diubah jadi: \`${newPassword}\``, { parse_mode: 'Markdown' });
        }
    } catch (err) {
        ctx.reply(`❌ Error server: ${err.message}`);
    }
});

bot.command('setexpiry', async (ctx) => {
    const args = ctx.message.text.split(' ');
    if (args.length < 3) {
        return ctx.reply('❌ Format salah. Gunakan: `/setexpiry <unique_id> <jumlah_hari>` (0 = unlimited)', { parse_mode: 'Markdown' });
    }

    const uniqueId = args[1].trim();
    const days = parseInt(args[2].trim());

    if (isNaN(days)) {
        return ctx.reply('❌ Jumlah hari harus angka! Contoh: `/setexpiry abc123 7`', { parse_mode: 'Markdown' });
    }

    let expiryDate = null;
    if (days > 0) {
        expiryDate = new Date();
        expiryDate.setDate(expiryDate.getDate() + days);
    } else {
        expiryDate = null;
    }

    try {
        const { data: checkUser, error: checkError } = await supabase
            .from('users')
            .select('id')
            .eq('unique_id', uniqueId);

        if (checkError || !checkUser || checkUser.length === 0) {
            return ctx.reply(`❌ Gagal: ID \`${uniqueId}\` gak ditemukan di database!`, { parse_mode: 'Markdown' });
        }

        const { error } = await supabase
            .from('users')
            .update({ expires_at: expiryDate })
            .eq('unique_id', uniqueId);

        if (error) {
            ctx.reply(`❌ Gagal update waktu: ${error.message}`);
        } else {
            const msgExpiry = days > 0 ? `berlaku selama ${days} hari (sampai ${expiryDate.toLocaleString()})` : 'UNLIMITED (abadi)';
            ctx.reply(`✅ Akses untuk ID \`${uniqueId}\` berhasil diubah menjadi: *${msgExpiry}*`, { parse_mode: 'Markdown' });
        }
    } catch (err) {
        ctx.reply(`❌ Error server: ${err.message}`);
    }
});

bot.command('deluser', async (ctx) => {
    const args = ctx.message.text.split(' ');
    if (args.length < 2) {
        return ctx.reply('❌ Format salah. Gunakan: `/deluser <unique_id>`', { parse_mode: 'Markdown' });
    }

    const uniqueId = args[1].trim();

    try {
        const { data: checkUser, error: checkError } = await supabase
            .from('users')
            .select('id')
            .eq('unique_id', uniqueId);

        if (checkError || !checkUser || checkUser.length === 0) {
            return ctx.reply(`❌ Gagal: ID \`${uniqueId}\` gak ditemukan di database!`, { parse_mode: 'Markdown' });
        }

        const { error, count } = await supabase
            .from('users')
            .delete()
            .eq('unique_id', uniqueId);

        if (error) {
            ctx.reply(`❌ Gagal menghapus user: ${error.message}`);
        } else {
            ctx.reply(`✅ User dengan ID \`${uniqueId}\` berhasil dihapus dari database.`, { parse_mode: 'Markdown' });
        }

    } catch (err) {
        ctx.reply(`❌ Error server: ${err.message}`);
    }
});

bot.help((ctx) => {
    ctx.reply(`
*📋 PANDUAN BOT CLIENT*
1. Ganti Password:
   \`/setpassword <unique_id> <password_baru>\`
2. Atur Waktu Kedaluwarsa (0 = Unlimited):
   \`/setexpiry <unique_id> <jumlah_hari>\`
3. Hapus User (Delete):
   \`/deluser <unique_id>\`
4. Lihat Daftar User (5 per halaman):
   \`/listuser\`
Contoh: \`/deluser abc123\`
    `, { parse_mode: 'Markdown' });
});

bot.launch().then(() => {
    console.log(`🤖 Bot Client dengan Telegraf berjalan! Owner ID: ${OWNER_ID}`);
}).catch((err) => {
    console.error("🚨 Gagal launch bot:", err);
});

process.once('SIGINT', () => bot.stop('SIGINT'));
process.once('SIGTERM', () => bot.stop('SIGTERM'));
