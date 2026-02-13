## Add
Add-deco_helper = Este subcomando é usado para adicionar uma anotação.
Add-deco_usage = Como usar: { $prefix }note add (texto)
Add-deco_description = Este comando serve para adicionar uma anotação.

# Add Examples
Add-cmd_ex1_args = add Uma anotação sobre algo que eu quero lembrar para sempre.
Add-cmd_ex1_res = Anotação criada com sucesso. 📝 (ID: <ID da nota>)
Add-cmd_ex2_args = add title:"Título para facilitar" Uma anotação sobre algo que eu quero lembrar para sempre.
Add-cmd_ex2_res = Anotação criada com sucesso. 📝 (ID: <ID da nota>)

# Add Admonitions
Add-adm1_title = Limite máximo de caracteres para 'add'!
Add-adm1_msg = A mensagem não pode exceder 450 caracteres. Se exceder, um erro será retornado.
Add-adm2_title = Limite máximo para o título!
Add-adm2_msg = O título não pode ter mais de 32 caracteres. Se exceder, um erro será retornado.
Add-adm3_title = Notas e Aliases
Add-adm3_msg = Use aliases e notas juntos para criar comandos personalizados. Por exemplo, com `{ $prefix }alias add bolo note check <id>`, você pode usar `{ $prefix }{ $prefix }bolo` para que o bot envie automaticamente o conteúdo da anotação, sem precisar digitar o comando completo `note check <id>`.

## Check
Check-deco_helper = Este subcomando é usado para verificar uma anotação.
Check-deco_usage = Como usar: { $prefix }note check (id)
Check-deco_description = Este comando serve para consultar uma anotação.

# Check Examples
Check-cmd_ex1_args = check
Check-cmd_ex1_res = Suas anotações são: <título se houver [id]>
Check-cmd_ex2_args = check <id>
Check-cmd_ex2_res = <Conteúdo da anotação.>

## Delete
Delete-deco_helper = Este subcomando é usado para deletar uma anotação.
Delete-deco_usage = Como usar: { $prefix }note delete (id)
Delete-deco_description = Este comando serve para excluir uma anotação.

# Delete Examples
Delete-cmd_ex1_args = delete <id>
Delete-cmd_ex1_res = Sua anotação com ID <id> foi excluída com sucesso. 🗑

## Annotations (Base)
Annotations-title_too_long = O título deve ter um máximo de 32 caracteres.
Annotations-too_few_characters = Você se esqueceu de enviar o conteúdo da anotação.
Annotations-annotation_created = Nota criada com sucesso. 📝 (ID: { $note_id })
Annotations-no_annotations_with_id = Você não tem nenhuma anotação com ID { $note_id }.
Annotations-all_annotations = Suas anotações são aquelas com ID: { $note_id }
Annotations-annotation_content = { $content }
Annotations-deleted = Sua anotação com ID { $note_id } foi excluída com sucesso. 🗑
Annotations-option_not_recognized = As opções válidas são apenas "add" "check" "delete"
Annotations-no_annotation_present = Você não tem nenhuma anotação salva.
Annotations-deco_helper = Cria notas permanentes para o usuário.
Annotations-deco_usage = Para usar: { $prefix }note add/check/delete
Annotations-deco_description = Cria notas permanentes para o usuário.
